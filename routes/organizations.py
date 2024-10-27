from typing import List
from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException,status
from beanie.operators import Set

from models import Organization, User
import models
import oauth2
import schemas

router = APIRouter()

##Organization

@router.post("",  status_code = status.HTTP_201_CREATED)
async def create_organization(organization: schemas.Organization = Body(),
                               current_user: int = Depends(oauth2.get_current_user)):
    p = {"name": organization.name,
                                             "description": organization.description, 
                                             "created_by": -1}
    new_organization = models.Organization(**p)

    await new_organization.insert()
    print(new_organization)
    
    return {"organization_id": new_organization.id}
    

@router.get("/{organization_id}", response_model=schemas.OrganizationWithUsers)
async def get_organization(organization_id: UUID, current_user: int = Depends(oauth2.get_current_user)):
    organization = await Organization.get(str(organization_id))
    
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Fetch users linked to the organization using organization_id
    organization_members = await User.find(User.organization_id == organization_id).to_list()  
    
    # Convert to desired output format (e.g., UserOut schema)
    organization_with_members = schemas.OrganizationWithUsers(
        **organization.dict(), 
        organization_members=[schemas.UserOrganization(**member.dict()) for member in organization_members]
    )
    
    return organization_with_members
    
@router.get("", response_model=List[schemas.Organization])
async def get_all_organizations( current_user: int = Depends(oauth2.get_current_user))-> List[Organization]:
    organizations = await Organization.find_all().to_list()
    
    return organizations

@router.put("/{organization_id}")
async def update_organization(organization_id: str, 
                              organization_new_data: schemas.Organization = Body(),
                               current_user: int = Depends(oauth2.get_current_user)):
        # Check if the organization exists first
    organization = await Organization.get(organization_id)
    print(organization)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    await organization.update(
        Set({
            Organization.name: organization_new_data.name,
            Organization.description: organization_new_data.description
        })
    )

    return organization
    

@router.delete("/{organization_id}", response_model = schemas.ResponseOut, status_code=status.HTTP_200_OK)
async def delete_organization(organization_id: str,  
                              current_user: int = Depends(oauth2.get_current_user)):
    organization = await Organization.get(organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
   
    await organization.delete()

    return schemas.ResponseOut(message=f"Organization with {organization_id} deleted successfully")

@router.post("{organization_id}/invite")
async def user_invite(organisation_id: str,
                      user_email_model: schemas.UserInvite = Body(),
                        current_user: int = Depends(oauth2.get_current_user)):
    
    user = await models.User.find_one(models.User.email == user_email_model.user_email)
    print(user)

    organization = await models.Organization.get(organisation_id)
    print(organization.id)
    if user and organization:
        user.organization_id = organization.id
        await user.save()