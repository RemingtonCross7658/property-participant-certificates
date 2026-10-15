"""Run the certificate example with INFRAI_API_KEY in the environment."""

from certificate_service import Participant, generate_certificate


if __name__ == "__main__":
    participant = Participant("Amina Chen", 3, 2, 1)
    result = generate_certificate(participant)
    print(result)
