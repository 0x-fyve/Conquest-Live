from .models import Participant

class ParticipantService():
    @staticmethod
    def create_or_update_participant(competition,
        external_id,
        display_name,
        metadata=None,
        ):

        if metadata is None:
            metadata = {}
        participant, created = Participant.objects.get_or_create(
            competition=competition,
            external_id=external_id,
            defaults={
                "display_name": display_name,
                "metadata": metadata
            }
        )  

        if not created:
            participant.display_name = display_name
            participant.metadata = metadata
            participant.save(update_fields=["display_name", "metadata"])

        return participant

