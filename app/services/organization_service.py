from fastapi.responses import JSONResponse
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession
from repository.organization_repository import OrganizationRepository
from repository.membership_repository import MembershipRepository

class OrganizationService:
    def __init__(self, organization_repository: OrganizationRepository, membership_repository: MembershipRepository):
        self.organization_repository = organization_repository
        self.membership_repository = membership_repository

    async def create_organization(self, user_id: int, name: str, db: AsyncSession):
        try:
            existing_organization = await self.organization_repository.get_organization_by_name(name, db)
            if existing_organization:
                return JSONResponse(
                    status_code=HTTPStatus.CONFLICT,
                    content={"message": "Organization with this name already exists."}
                )

            user_membership = await self.membership_repository.get_membership_by_user_id_and_role(user_id, 'admin', db)
            if user_membership:
                return JSONResponse(
                    status_code=HTTPStatus.CONFLICT,
                    content={"message": "User already has an organization with admin role."}
                )
            

            new_organization = await self.organization_repository.create_organization(name, db)
            

            new_membership = await self.membership_repository.create_membership(user_id, new_organization.id, 'admin', db)

            return JSONResponse(
                status_code=HTTPStatus.CREATED,
                content={"message": "Organization created successfully", "organization_name": new_organization.name}
            )
        except Exception as e:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"message": f"Internal server error. ERROR: {e}"}
            )
