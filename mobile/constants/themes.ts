export const INTERESTS = [
  { id: "animals", label: "Animals", emoji: "🐾" },
  { id: "space", label: "Space", emoji: "🚀" },
  { id: "dinosaurs", label: "Dinosaurs", emoji: "🦕" },
  { id: "ocean", label: "Ocean", emoji: "🌊" },
  { id: "nature", label: "Nature", emoji: "🌿" },
  { id: "music", label: "Music", emoji: "🎵" },
  { id: "art", label: "Art", emoji: "🎨" },
  { id: "vehicles", label: "Vehicles", emoji: "🚗" },
  { id: "fairies", label: "Fairies", emoji: "🧚" },
  { id: "robots", label: "Robots", emoji: "🤖" },
  { id: "cooking", label: "Cooking", emoji: "🍳" },
  { id: "sports", label: "Sports", emoji: "⚽" },
  { id: "princesses", label: "Princesses", emoji: "👸" },
  { id: "pirates", label: "Pirates", emoji: "🏴‍☠️" },
  { id: "bugs", label: "Bugs", emoji: "🐛" },
  { id: "weather", label: "Weather", emoji: "⛅" },
  { id: "trains", label: "Trains", emoji: "🚂" },
  { id: "magic", label: "Magic", emoji: "✨" },
] as const;

export const LANGUAGES = [
  { code: "en", label: "English", flag: "🇺🇸" },
  { code: "es", label: "Spanish", flag: "🇪🇸" },
  { code: "zh", label: "Chinese", flag: "🇨🇳" },
  { code: "fr", label: "French", flag: "🇫🇷" },
  { code: "de", label: "German", flag: "🇩🇪" },
  { code: "ja", label: "Japanese", flag: "🇯🇵" },
  { code: "ko", label: "Korean", flag: "🇰🇷" },
] as const;

export const STORY_STYLES = [
  { id: "", label: "Default", description: "Gentle and calming" },
  { id: "goodnight-moon", label: "Like Goodnight Moon", description: "Calm and repetitive" },
  { id: "curious-george", label: "Like Curious George", description: "Exploration & curiosity" },
  { id: "pete-cat", label: "Like Pete the Cat", description: "Cool and laid-back" },
  { id: "hungry-caterpillar", label: "Like Very Hungry Caterpillar", description: "Repetitive & counting" },
] as const;

export const CREDIT_PACKS = [
  { id: "10", credits: 10, price: "$4.99", perStory: "$0.50" },
  { id: "25", credits: 25, price: "$9.99", perStory: "$0.40" },
  { id: "50", credits: 50, price: "$14.99", perStory: "$0.30" },
  { id: "100", credits: 100, price: "$24.99", perStory: "$0.25" },
] as const;

export const SUBSCRIPTION_PLANS = [
  {
    id: "premium",
    name: "Premium",
    price: "$9.99/mo",
    features: [
      "Unlimited stories",
      "Premium voices",
      "5 kid profiles",
      "Illustrations",
      "No ads",
      "Parent dashboard",
    ],
  },
  {
    id: "family",
    name: "Family",
    price: "$14.99/mo",
    features: [
      "Everything in Premium",
      "Voice cloning",
      "10 profiles",
      "Offline packs",
      "Story sharing",
    ],
  },
] as const;
