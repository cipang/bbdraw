from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from random import choice
from .models import Team, Slot


def free_teams(request):
    allocated_teams = Slot.objects.exclude(chosen=None).values_list("chosen_id", flat=True)
    qs = Team.objects.exclude(pk__in=allocated_teams)
    result = [{"id": x.id, "name": x.name} for x in qs]
    return JsonResponse({"teams": result})


def draw_next(request):
    all_slots = list(Slot.objects.all())
    free_slots = list(Slot.objects.filter(chosen=None))

    team = get_object_or_404(Team, id=request.GET.get("t", -1) or None)
    filter_slots(team, all_slots, free_slots)

    print("Before", team, free_slots)
    if not free_slots:
        return HttpResponseBadRequest("No more free slots.")

    display = list()
    for i in range(0, 20):
        candidates = [x for x in all_slots if x.key != display[-1]] if i > 0 \
            else all_slots
        display.append(choice(candidates).key)

    chosen_slot = choice(free_slots)
    chosen_slot.chosen = team
    chosen_slot.save()
    display.append(chosen_slot.key)

    print("After", team, chosen_slot)
    return JsonResponse({"display": display, "slot": chosen_slot.key})


def filter_slots(team, all_slots, free_slots):
    flag = team.flag
    if not flag:
        return

    # Find the group prefixes with teams having the same flag.
    removable = {slot.key[0] for slot in all_slots
                 if slot.chosen and slot.chosen.flag == flag}

    backup = list(free_slots)
    # Delete any free slots in the same group.
    free_slots[:] = [slot for slot in free_slots
                     if slot.key[0] not in removable]

    if not free_slots:
        free_slots[:] = backup
