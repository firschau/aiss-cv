import classes
from slots import Slots


#state = State()
slots = Slots()


# Return statements are added, so that it if the first if condition is true, it doesn't check the rest
def slot_logic(prediction):
    #TODO: What do we do with End Speed Restriction Class?

    if isinstance(prediction, classes.Slot1):
        slots.update_slot1(prediction)
        return

    if isinstance(prediction, classes.Slot2):
        slots.update_slot2(prediction)
        return

    if isinstance(prediction, classes.Slot3):
        slots.update_slot3(prediction)
        return

    if isinstance(prediction, classes.Slot4):
        slots.update_slot4(prediction)
        return

    if isinstance(prediction, classes.EndRestrict):
        if prediction == classes.EndRestrict.END_OVERTAKING:
            if slots.slot2 == classes.Overtaking.NO_OVERTAKING:
                slots.update_slot2(prediction)
                return



"""
# FUNCTION OLD PROBABLY NOT USEFUL
# Return statements are added, so that it if the first if condition is true, it doesn't check the rest
def state_logic(prediction):
    if isinstance(prediction, classes.SpeedLimit):
        state.update_speed_limit(prediction)
        slots.update_slot1(state.speed_limit)  #TODO: Maybe in different logic function
        return

    if isinstance(prediction, classes.EndRestrict):
        if prediction == classes.EndRestrict.END_80:
            if state.speed_limit == classes.SpeedLimit.LIMIT_80:
                placeholder = None
                # TODO: WHAT DO WE DOOOOOOO?!?!??!?!??
                return

        if prediction == classes.EndRestrict.END_ALL:
            # TODO: state.update_speed_limit... AGAIN WHAT DO WE DO WITH THE SPEED LIMIT??!?!??!
            state.update_no_overtaking(None) # TODO: I don't know if None is fine maybe define a blank variable
            return

        if prediction == classes.EndRestrict.END_OVERTAKING:
            if state.no_overtaking == classes.Overtaking.NO_OVERTAKING:
                state.update_no_overtaking(None)
                return

        if prediction == classes.EndRestrict.END_OVERTAKING_T:
            if state.no_overtaking == classes.Overtaking.NO_OVERTAKING_T:
                state.update_no_overtaking(None)
                return

    if isinstance(prediction, classes.Instruction):
        state.update_instruction(prediction)
        return

    if isinstance(prediction, classes.DangerLong):
        state.update_danger_long(prediction)
        return

    if isinstance(prediction, classes.DangerShort):
        state.update_danger_short(prediction)
        return

    if isinstance(prediction, classes.Overtaking):
        state.update_no_overtaking(prediction)
        return

    if isinstance(prediction, classes.GiveWay):
        state.update_give_way(prediction)
        return

    if isinstance(prediction, classes.Parking):
        state.update_no_parking(prediction)
        return

    if isinstance(prediction, classes.Person):
        state.update_person(prediction)

"""
