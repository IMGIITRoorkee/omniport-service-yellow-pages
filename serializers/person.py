import swapper
from rest_framework import serializers

Person = swapper.load_model('kernel', 'Person')

class PersonIDSerializer(serializers.ModelSerializer):
    """
    Serializer for ids of person objects
    """

    class Meta:
        """
        Meta class for PersonIDSerializer
        """

        model = Person
        fields = [
            "id",
        ]