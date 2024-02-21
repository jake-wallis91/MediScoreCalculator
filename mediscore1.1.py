from enum import Enum
from datetime import datetime, timedelta


class AirOrOxygen(Enum):
    AIR = 0
    OXYGEN = 2


class Consciousness(Enum):
    ALERT = 0
    CVPU = 1


class CBGTiming(Enum):
    FASTING = "fasting"
    AFTER_EATING = "after_eating"


class Patient:
    def __init__(self, oxygen_requirement, consciousness_score, respiration_rate, spo2, temperature, cbg_value,
                 cbg_timing):
        self.oxygen_requirement = AirOrOxygen(oxygen_requirement)
        self.consciousness_score = Consciousness(consciousness_score)
        self.respiration_rate = respiration_rate
        self.spo2 = spo2
        self.temperature = temperature
        self.cbg_value = cbg_value
        self.cbg_timing = cbg_timing
        self.individual_scores = {}  # Dictionary to store individual scores
        self.medi_scores = [(datetime.now(), 0)]  # Initialize with current time and initial Medi score

    def calculate_cbg_score(self):
        cbg_score = 0
        cbg_value = self.cbg_value

        if self.cbg_timing == CBGTiming.FASTING:
            if cbg_value <= 3.4:
                cbg_score = 3
            elif 3.5 <= cbg_value <= 3.9:
                cbg_score = 2
            elif 4.0 <= cbg_value <= 5.4:
                cbg_score = 0
            elif 5.5 <= cbg_value <= 5.9:
                cbg_score = 2
            elif cbg_value >= 6.0:
                cbg_score = 3
            else:
                cbg_score = -1  # Out of range
        elif self.cbg_timing == CBGTiming.AFTER_EATING:
            if cbg_value <= 4.5:
                cbg_score = 3
            elif 4.5 <= cbg_value <= 5.8:
                cbg_score = 2
            elif 5.9 <= cbg_value <= 7.8:
                cbg_score = 0
            elif 7.9 <= cbg_value <= 8.9:
                cbg_score = 2
            elif cbg_value >= 9.0:
                cbg_score = 3
            else:
                cbg_score = -1  # Out of range

        return cbg_score

    def calculate_medi_score(self):
        medi_score = 0

        # Calculate score for oxygen requirement
        oxygen_score = self.oxygen_requirement.value
        self.individual_scores['oxygen_requirement'] = oxygen_score
        medi_score += oxygen_score

        # Add score for consciousness
        consciousness_score = self.consciousness_score.value
        self.individual_scores['consciousness_score'] = consciousness_score
        medi_score += consciousness_score

        # Calculate score for respiration rate
        if self.respiration_rate <= 8:
            respiration_score = 3
        elif 9 <= self.respiration_rate <= 11:
            respiration_score = 1
        elif 21 <= self.respiration_rate <= 24:
            respiration_score = 2
        elif self.respiration_rate >= 25:
            respiration_score = 3
        else:
            respiration_score = 0
        self.individual_scores['respiration_rate'] = respiration_score
        medi_score += respiration_score

        # Calculate score for SpO2 based on oxygen requirement
        if self.oxygen_requirement == AirOrOxygen.OXYGEN:  # Patient is on oxygen
            if self.spo2 <= 83:
                spo2_score = 3
            elif 84 <= self.spo2 <= 85:
                spo2_score = 2
            elif 86 <= self.spo2 <= 87:
                spo2_score = 1
            elif 88 <= self.spo2 <= 92:
                spo2_score = 0
            elif 93 <= self.spo2 <= 94:
                spo2_score = 1
            elif 95 <= self.spo2 <= 96:
                spo2_score = 2
            elif self.spo2 >= 97:
                spo2_score = 3
        else:  # Patient is breathing air
            if self.spo2 <= 83:
                spo2_score = 3
            elif 84 <= self.spo2 <= 85:
                spo2_score = 2
            elif 86 <= self.spo2 <= 87:
                spo2_score = 1
            elif 88 <= self.spo2 <= 93:
                spo2_score = 0
            elif 93 <= self.spo2 <= 94:
                spo2_score = 0
            elif 95 <= self.spo2 <= 96:
                spo2_score = 0
            elif self.spo2 >= 97:
                spo2_score = 0
        self.individual_scores['spo2'] = spo2_score
        medi_score += spo2_score

        # Calculate score for temperature
        if self.temperature <= 35.0:
            temperature_score = 3
        elif 35.1 <= self.temperature <= 36.0:
            temperature_score = 1
        elif 38.1 <= self.temperature <= 39.0:
            temperature_score = 1
        elif self.temperature >= 39.1:
            temperature_score = 2
        else:
            temperature_score = 0
        self.individual_scores['temperature'] = temperature_score
        medi_score += temperature_score

        # Add CBG score
        cbg_score = self.calculate_cbg_score()
        self.individual_scores['cbg_score'] = cbg_score
        medi_score += cbg_score

        # Update Medi scores
        self.medi_scores.append((datetime.now(), medi_score))

        return medi_score

    def has_score_increased(self):
        if len(self.medi_scores) < 2:
            return False

        # Check the score difference between the most recent and previous score
        recent_score = self.medi_scores[-1][1]
        previous_score = self.medi_scores[-2][1]
        score_difference = recent_score - previous_score

        # Check if score has increased by more than 2 points within a 24-hour period
        if score_difference > 2 and (self.medi_scores[-1][0] - self.medi_scores[-2][0]) <= timedelta(days=1):
            return True
        else:
            return False


# Example patients with CBG measurements
patient1 = Patient(0, 0, 15, 95, 37.1, 4.8, CBGTiming.FASTING)
patient2 = Patient(2, 0, 17, 95, 37.1, 6.3, CBGTiming.AFTER_EATING)
patient3 = Patient(2, 1, 23, 88, 38.5, 5.0, CBGTiming.FASTING)
patient4 = Patient(2, 1, 11, 86, 35.5, 4.6, CBGTiming.AFTER_EATING)

# Calculate Medi scores for each patient
patient1_score = patient1.calculate_medi_score()
patient2_score = patient2.calculate_medi_score()
patient3_score = patient3.calculate_medi_score()
patient4_score = patient4.calculate_medi_score()

# Print Medi scores for each patient
print("Patient 1 Final Medi Score:", patient1_score)
print("Patient 2 Final Medi Score:", patient2_score)
print("Patient 3 Final Medi Score:", patient3_score)
print("Patient 4 Final Medi Score:", patient4_score)

# Print individual scores for each patient
print("\nIndividual Scores:")
print("Patient 1:")
for key, value in patient1.individual_scores.items():
    print(f"{key.replace('_', ' ').title()}: {value}")
print("\nPatient 2:")
for key, value in patient2.individual_scores.items():
    print(f"{key.replace('_', ' ').title()}: {value}")
print("\nPatient 3:")
for key, value in patient3.individual_scores.items():
    print(f"{key.replace('_', ' ').title()}: {value}")
print("\nPatient 4:")
for key, value in patient4.individual_scores.items():
    print(f"{key.replace('_', ' ').title()}: {value}")

# Check if scores have increased for each patient
print("\nScore Increase Status:")
print("Patient 1 Score Increased:", patient1.has_score_increased())
print("Patient 2 Score Increased:", patient2.has_score_increased())
print("Patient 3 Score Increased:", patient3.has_score_increased())
print("Patient 4 Score Increased:", patient4.has_score_increased())
