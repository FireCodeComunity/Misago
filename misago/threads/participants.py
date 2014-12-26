from misago.threads.models import ThreadParticipant


def make_thread_participants_aware(user, thread):
    thread.participants_list = []
    thread.participant = None

    participants_qs = ThreadParticipant.objects.filter(thread=thread)
    participants_qs = participants_qs.select_related('user')
    for participant in participants_qs.order_by('-is_owner', 'user__slug'):
        participant.thread = thread
        thread.participants_list.append(participant)
        if participant.user == user:
            thread.participant = participant
    return thread.participants_list


def thread_has_participants(thread):
    return thread.threadparticipant_set.exists()


def set_thread_owner(thread, user):
    ThreadParticipant.objects.set_thread_owner(thread, user)


def sync_user_unread_private_threads(user):
    user.sync_unread_private_threads = True
    user.save(update_fields=['sync_unread_private_threads'])


def add_participant(request, thread, user, is_owner=False):
    """
    Add participant to thread, set "recound private threads" flag on user,
    notify user about being added to thread and mail him about it
    """
    ThreadParticipant.objects.add_participant(thread, user, is_owner)
    sync_user_unread_private_threads(user)


def remove_participant(thread, user):
    """
    Remove thread participant, set "recound private threads" flag on user
    """
    thread.threadparticipant_set.filter(user=user).delete()
    sync_user_unread_private_threads(user)
