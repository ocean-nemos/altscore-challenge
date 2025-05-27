# Challenge: Uncovering the Cost of Living in the Galactic Empire

## The Story Begins

> In the shadow of the Galactic Empire, a quiet Rebellion is brewing. The grip of Imperial rule is tightening, and planets across the galaxy are struggling under the burden of rising costs. Desperate for answers, the Rebellion has launched a covert operation to uncover the truth behind the Empire's hidden economic control.
> 
> The Emperor's propaganda claims prosperity, but secret data tells a different story—a story only the best intelligence officers can decipher. The Rebellion needs you to become a hero. The fate of star systems hangs in the balance, and every byte of data you uncover brings the galaxy one step closer to freedom.

---

## Your Mission

As a newly recruited Rebel intelligence officer, you've been granted access to highly classified mobility data intercepted from the Empire's network. Your task is to analyze this information, predicting the true cost of living for regions across the galaxy. Each prediction could be a turning point in the struggle against Imperial oppression.

The data is encrypted using the Galactic Council's powerful H3 geospatial grid—an advanced system known for its precision. With the clock ticking, you must decode the movement patterns, extract insights, and accurately estimate the cost of living in each sector before the Empire discovers your mission.

Only the most skilled and insightful intelligence officers will succeed. The competition is fierce, and only those who can wield the power of data with precision and creativity will prevail.

## The Tools of Rebellion

The Rebellion's intelligence arm has provided you with a set of encrypted data files. These are the tools you'll need to expose the Empire's deception:

* **train.csv** - Data from sectors already liberated by the Rebellion. Each entry contains precise coordinates and the true cost of living, encrypted by the Galactic Council's H3 technology.
* **test.csv** - Sectors still under Imperial control, awaiting your predictions to reveal the hidden cost of living.
* **mobility.parquet** - A data set containing the secret movement patterns of operatives, smugglers, and civilians across the galaxy. These movements hold the clues to understanding the local economies of each region.

## The Power of Prediction

The Rebellion isn't just looking for predictions—they're seeking **insights**. Your mission is not only to estimate the cost of living but to **transform chaos into clarity**. The Empire's secrets are buried in raw data, waiting for you to uncover the truth. Use creativity, strategic feature engineering, and any additional data you can find to strengthen the Rebellion's cause.

## Guidance for the Rebellion

The Rebellion values creativity and courage. While accuracy is crucial, your true worth lies in the features you engineer and the insights you derive from the data. Be brave, think outside the box, and let the Force guide your analysis. **Only the best will make it through**—will you rise to the challenge?

Below is a snippet of code to help you decrypt the Imperial coordinates:

```python
# Example code snippet to convert galactic coordinates to H3 index
import h3

latitude = 37.7749  # Example coordinate
longitude = -122.4194  # Example coordinate
resolution = 9  # H3 encryption level

h3_index = h3.latlng_to_cell(latitude, longitude, resolution)
print(f"H3 Index: {h3_index}")
```

## How to join the Rebellion

Your journey begins here, but it doesn't end until you've faced the ultimate test. Prove your loyalty to the Rebellion by participating in the official challenge on the Rebellion's covert platform—**Kaggle**. The true cost of freedom lies in your data analysis skills.

---

## May the Data Be with You!

Every prediction you make, every insight you extract, every feature you engineer could tip the scales in the galaxy's favor. The Rebellion needs your brilliance, creativity, and determination. The Emperor's grip tightens with each passing moment—act quickly, and together, we will bring balance to the galaxy.

Only the most capable will earn the title of the Rebellion's top intelligence officer. Are you one of them?

[Join the Kaggle Competition](https://www.kaggle.com/competitions/alt-score-data-science-competition)
