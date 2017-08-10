from .models import Program, Member
from django.shortcuts import get_object_or_404

def _retrieve_member(request, program_id):
    """
    Get the member record of the current user and program_id
    """
    user = request.user or None
    if not user or not program_id:
        return None
    try:
        program = get_object_or_404(Program, pk=program_id)
        member = get_object_or_404(Member, user=user, program=program)
    except:
        return None


def _add_organization_to_session(request, organization_id):
    """
    Returns the organization's id when successful or None if session
    is non-existent
    """
    if request.session:
        request.session['organization_id'] = organization_id
        return organization_id
    return None


def _is_current_organization(request, organization_id):
    """
    Return a boolean: True when this is the current organization
    """
    if request.session:
        session_org_id = request.session.get('organization_id') or None
        if session_org_id:
            return organization_id == session_org_id

    return False


def update_session_organization(request, organization_id):
    """
    Every time a user selects an organization, this function is called
    """
    if not _is_current_organization(request, organization_id):
        return _add_organization_to_session(request, organization_id)

    return True


def _add_program_to_session(request, program_id):
    """
        Returns the program's id when successful or None if session
        is non-existent
        """
    if request.session:
        request.session['program_id'] = program_id
        return program_id
    return None


def _is_current_program(request, program_id):
    """
    Return a boolean: True when this is the current organization
    """
    if request.session:
        session_program_id = request.session.get('program_id') or None
        if session_program_id:
            return program_id == session_program_id

    return False


def update_session_program(request, program_id):
    """
    Every time a user selects a program, this function is called
    """
    if not _is_current_program(request, program_id):
        return _add_program_to_session(request, program_id)

    return True


def get_current_member(request):
    if request.session:
        program_id = request.session.get('program_id') or None
        user = request.user or None
        return _retrieve_member(user, program_id)
    return None


def save_member_to_session(request):
    """
    Returns the member_id when successful and None if session or member
    are non-existent
    """
    if request.session:
        member = get_current_member(request)
        if member and member.id:
            member_id = request.session.get('member_id') or None

            # add the member to session if not in session
            if not member_id:
                request.session['member_id'] = member.id

            # update the session variable if it is not current
            if not member_id == member.id:
                request.session['member_id'] = member.id

            return member.id

    return None
