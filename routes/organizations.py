from typing import List
from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException, status
from beanie.operators import Set

from models import AccessLevel, Organization, User
import models
import oauth2
import schemas

router = APIRouter()

##Organization


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_organization(
    organization: schemas.Organization = Body(),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    """
    A route with POST method to Create a new organization

    """

    org = {
        "name": organization.name,
        "description": organization.description,
    }

    new_organization = models.Organization(**org)
    await new_organization.insert()

    await current_user.update(
        Set(
            {
                User.organization_id: new_organization.id,
                User.access_level: AccessLevel.admin.value,
            }
        )
    )
    return {"organization_id": new_organization.id}


@router.get("/{organization_id}", response_model=schemas.OrganizationWithUsers)
async def get_organization(
    organization_id: UUID, current_user: models.User = Depends(oauth2.get_current_user)
):
    """

    A route with GET method to Get an organization by id

    """
    organization = await Organization.get(str(organization_id))

    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    # Fetch users linked to the organization using organization_id
    organization_members = await User.find(
        User.organization_id == organization_id
    ).to_list()

    # Convert to desired output format (e.g., UserOut schema)
    organization_with_members = schemas.OrganizationWithUsers(
        **organization.dict(),
        organization_members=[
            schemas.UserOrganization(**member.dict()) for member in organization_members
        ],
    )

    return organization_with_members


@router.get("", response_model=List[schemas.Organization])
async def get_all_organizations(
    current_user: models.User = Depends(oauth2.get_current_user),
) -> List[Organization]:
    """

    A route with GET method to Get all organizations

    """
    organizations = await Organization.find_all().to_list()

    return organizations


@router.put("/{organization_id}")
async def update_organization(
    organization_id: str,
    organization_new_data: schemas.Organization = Body(),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    """

    A route with UPDATE method to Update organization by id

    """
    # Check if the organization exists first
    organization = await Organization.get(organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    if current_user.access_level == "member" or str(organization_id) != str(
        current_user.organization_id
    ):
        raise HTTPException(status_code=401, detail="Unauthorized")

    await organization.update(
        Set(
            {
                Organization.name: organization_new_data.name,
                Organization.description: organization_new_data.description,
            }
        )
    )

    return organization


@router.delete(
    "/{organization_id}",
    response_model=schemas.ResponseOut,
    status_code=status.HTTP_200_OK,
)
async def delete_organization(
    organization_id: str, current_user: models.User = Depends(oauth2.get_current_user)
):
    """

    A route with DELETE method to Delete organization by id

    """
    organization = await Organization.get(organization_id)

    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    if current_user.access_level == "member" or str(organization_id) != str(
        current_user.organization_id
    ):
        raise HTTPException(status_code=401, detail="Unauthorized")
    await organization.delete()

    return schemas.ResponseOut(
        message=f"Organization with {organization_id} deleted successfully"
    )


@router.post("{organization_id}/invite")
async def user_invite(
    organisation_id: str,
    user_email_model: schemas.UserInvite = Body(),
    current_user: models.User = Depends(oauth2.get_current_user),
):

    user = await models.User.find_one(models.User.email == user_email_model.user_email)
    organization = await models.Organization.get(organisation_id)
    if user and organization:
        user.organization_id = organization.id
        await user.save()
