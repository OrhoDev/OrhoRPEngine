# --- START OF FILE world.py ---

CORE_PHYSICS = """
1. The Nature of Cursed Energy and Curses
- Cursed Energy (Juryoku): A fundamental, volatile energy source derived directly from negative human emotions. It flows throughout the body like electricity and serves as the power source for all jujutsu.
- Cursed Spirits (Jurei): Autonomous entities born from leaked cursed energy. They naturally aggregate in high-stress areas (schools, hospitals) to harm humanity.
- Sorcerers vs. Non-Sorcerers: Sorcerers possess a neural structure to control cursed energy and perceive curses; non-sorcerers leak energy and cannot see jujutsu phenomena.
- The Soul and the Body: The soul and body are intertwined; the soul's contours influence the body's shape. Soul damage cannot be healed by conventional RCT.
"""

GENERAL_MECHANICS = """
2. General World Rules and Mechanics
- Binding Vows (Shibari): Unbreakable pacts of equivalent exchange. Self-imposed restrictions boost power; violations carry lethal supernatural punishment.
- Heavenly Restriction (Tenyo Jubaku): Involuntary birth-vows. Strips cursed energy for god-like physical prowess, or vice-versa.
- Cursed Tools and Objects: Items imbued with cursed energy or the remains of powerful sorcerers. If ingested, cursed objects can allow a soul to incarnate into a vessel.
- Cursed Corpses (Jugai): Inanimate objects with an internal "core" of cursed energy, granting sentience and mobility.
"""

BARRIER_AND_ANTI_DOMAIN = """
3. Barrier Techniques and Anti-Domain Countermeasures
- Curtains / Veils (Tobari): Specialized barriers used to conceal jujutsu operations from the public.
- Simple Domain (Kan'i Ryoiki): A small barrier that neutralizes a hostile Domain's guaranteed-hit effect. It does not neutralize the opponent's technique itself.
- Hollow Wicker Basket (Miyo Kotsuzura): An ancient anti-domain technique requiring continuous hand signs to neutralize guaranteed-hits.
- Falling Blossom Emotion: A secret clan countermeasure that coats the body in reactive energy to auto-intercept guaranteed-hit attacks.
- Domain Amplification: A fluid "empty" domain that acts as a vacuum, sucking in and neutralizing any hostile technique it touches.
"""

ADVANCED_COMBAT = """
4. Advanced Techniques and Phenomena
- Domain Expansion (Ryoiki Tenkai): Materializing an "Innate Domain" into reality via a barrier. Grants massive stat buffs and a "guaranteed-hit" parameter to the user's technique. Causes "Technique Burnout" after deactivation.
- Incomplete Domain: A Domain Expansion without a closed barrier; lacks a guaranteed-hit but provides statistical amplification.
- Black Flash (Kokusen): A spatial distortion occurring when cursed energy is applied within 0.000001s of impact. destructive force is amplified to the power of 2.5. Plunges the sorcerer into "The Zone."
- Reverse Cursed Technique (RCT): Multiplying negative energy to create positive energy. Capable of regenerating flesh and regrowing limbs.
- Maximum Techniques (Gokunoban): The supreme martial application of an innate technique, representing its highest possible output.
"""

LOCATIONS_AND_POLITICS = """
5. Metaphysical and Physical Locations
- Tokyo/Kyoto Jujutsu High: The educational and administrative hubs of jujutsu society, hidden behind topological barriers.
- The Star Tombs (Tengen's Barriers): Deep subterranean architectures housing the foundational barrier arrays of Japan.
- Jujutsu Headquarters: The administrative core governed by conservative elders; drafts execution orders and assigns sorcerer grades.
"""

# The Master Dictionary for the Engine
JUJUTSU_WORLD = {
    "physics": CORE_PHYSICS,
    "mechanics": GENERAL_MECHANICS,
    "barriers": BARRIER_AND_ANTI_DOMAIN,
    "combat": ADVANCED_COMBAT,
    "locations": LOCATIONS_AND_POLITICS
}