from app.organizations.models.enums import (
    OrganizationMemberStatus,
    OrganizationRole,
)


class OrganizationPolicy:

    @staticmethod
    def can_view(
        role: OrganizationRole,
        status: OrganizationMemberStatus,
    ) -> bool:
        return status == OrganizationMemberStatus.ACTIVE

    @staticmethod
    def can_update(
        role: OrganizationRole,
        status: OrganizationMemberStatus,
    ) -> bool:
        if status != OrganizationMemberStatus.ACTIVE:
            return False

        return role in {
            OrganizationRole.OWNER,
            OrganizationRole.ADMIN,
        }

    @staticmethod
    def can_delete(
        role: OrganizationRole,
        status: OrganizationMemberStatus,
    ) -> bool:
        if status != OrganizationMemberStatus.ACTIVE:
            return False

        return role == OrganizationRole.OWNER

    @staticmethod
    def can_manage_members(
        role: OrganizationRole,
        status: OrganizationMemberStatus,
    ) -> bool:
        if status != OrganizationMemberStatus.ACTIVE:
            return False

        return role in {
            OrganizationRole.OWNER,
            OrganizationRole.ADMIN,
        }

    @staticmethod
    def can_view_members(
        role: OrganizationRole,
        status: OrganizationMemberStatus,
    ) -> bool:
        return status == OrganizationMemberStatus.ACTIVE

    @staticmethod
    def can_change_role(
        actor_role: OrganizationRole,
        target_role: OrganizationRole,
        new_role: OrganizationRole,
        actor_status: OrganizationMemberStatus,
        target_status: OrganizationMemberStatus,
    ) -> bool:
        if actor_status != OrganizationMemberStatus.ACTIVE:
            return False

        if target_status != OrganizationMemberStatus.ACTIVE:
            return False

        # Only OWNER can manage another ADMIN.
        if target_role == OrganizationRole.ADMIN:
            return actor_role == OrganizationRole.OWNER

        # OWNER cannot be changed through normal role management.
        if target_role == OrganizationRole.OWNER:
            return False

        # Only OWNER can assign OWNER.
        if new_role == OrganizationRole.OWNER:
            return False

        if actor_role == OrganizationRole.OWNER:
            return True

        if actor_role == OrganizationRole.ADMIN:
            return target_role in {
                OrganizationRole.MEMBER,
                OrganizationRole.VIEWER,
            }

        return False

    @staticmethod
    def can_suspend_member(
        actor_role: OrganizationRole,
        target_role: OrganizationRole,
        actor_status: OrganizationMemberStatus,
        target_status: OrganizationMemberStatus,
    ) -> bool:
        if actor_status != OrganizationMemberStatus.ACTIVE:
            return False

        if target_status != OrganizationMemberStatus.ACTIVE:
            return False

        # Owner cannot be suspended.
        if target_role == OrganizationRole.OWNER:
            return False

        # Only owner can suspend an admin.
        if target_role == OrganizationRole.ADMIN:
            return actor_role == OrganizationRole.OWNER

        # Owner can suspend members/viewers.
        if actor_role == OrganizationRole.OWNER:
            return True

        # Admin can suspend ordinary members/viewers.
        if actor_role == OrganizationRole.ADMIN:
            return target_role in {
                OrganizationRole.MEMBER,
                OrganizationRole.VIEWER,
            }

        return False

    @staticmethod
    def can_remove_member(
        actor_role: OrganizationRole,
        target_role: OrganizationRole,
        actor_status: OrganizationMemberStatus,
        target_status: OrganizationMemberStatus,
    ) -> bool:
        if actor_status != OrganizationMemberStatus.ACTIVE:
            return False

        if target_status != OrganizationMemberStatus.ACTIVE:
            return False

        # Owner cannot be removed through member management.
        if target_role == OrganizationRole.OWNER:
            return False

        # Only owner can remove an admin.
        if target_role == OrganizationRole.ADMIN:
            return actor_role == OrganizationRole.OWNER

        if actor_role == OrganizationRole.OWNER:
            return True

        if actor_role == OrganizationRole.ADMIN:
            return target_role in {
                OrganizationRole.MEMBER,
                OrganizationRole.VIEWER,
            }

        return False