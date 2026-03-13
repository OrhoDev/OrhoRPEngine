# --- START OF FILE techniques.py ---

TECHNIQUES_DB_LOCAL = {
    # --- HIROTO AKAGI ---
    "Legend Manifestation Technique": "Intercepts mythological archetypes from humanity's collective belief, binds them as shikigami. Permanent loss if destroyed in combat.",
    "Command Hierarchy": "Commands bound entities via Direct Command (precise), Tactical Command (goal-oriented), or Autonomous Mode (instinct-based).",
    "Technique Synergy": "Combines different mythological entities to create multi-elemental interactions.",
    "Below-Average Close Quarters Combat": "Backline controller. Highly vulnerable in melee. Relies on evasion and basic CE reinforcement only.",
    "Domain Expansion: Mythological Convergence Field": "Barrier domain saturating the area in mythological energy. Hiroto becomes secondary vessel for active shikigami, dual-casting their techniques. Extreme CE drain.",
    "Technique Convergence": "Domain effect. Duplicates every active technique — enemy fights the shikigami AND Hiroto using the same ability simultaneously.",

    # --- CHOSO ---
    "Blood Manipulation": "Controls own blood — shape, velocity, density. Forms projectiles or hardens for defense.",
    "Flowing Red Scale": "Raises blood pressure and body temperature for physical boost. Risks thrombosis.",
    "Flowing Red Scale: Stack": "Focuses boost into one body part — e.g. eyes for reaction speed.",
    "Supernova": "Compresses multiple blood projectiles into single explosive AoE release.",
    "Blood Meteorite": "Hardened blood projectile fired at high velocity.",

    # --- GETO ---
    "Cursed Spirit Manipulation": "Absorbs and stores cursed spirits by ingesting them. Deploys in battle.",
    "Uzumaki": "Releases multiple stored spirits simultaneously, combining their energy into a massive blast.",
    "Maximum: Uzumaki": "Uzumaki amplified using Special Grade stored spirits.",

    # --- GOJO ---
    "Limitless": "Mathematical concept of infinity brought into reality. Absolute spatial control at atomic level.",
    "Infinity": "Passive. Slows approaching objects infinitely — they never reach the user.",
    "Cursed Technique Lapse: Blue": "Localized vacuum of negative space. Forcefully attracts everything toward it.",
    "Cursed Technique Reversal: Red": "Condensed positive energy orb. Violently repels everything with explosive force.",
    "Hollow Technique: Purple": "Blue and Red collide — imaginary mass erases matter at atomic level.",
    "Six Eyes": "Ocular trait. Extraordinary perception, near-zero CE consumption.",
    "Domain Expansion: Unlimited Void": "Floods target's brain with infinite raw information. Instant catatonia.",

    # --- YUJI ---
    "Superhuman Physicals": "Abnormally dense muscle. Shatters concrete, superhuman speed without CE.",
    "Divergent Fist": "Physical strike lands first, lagging CE follows as secondary impact.",
    "Black Flash": "CE applied within 0.000001s of impact. Output multiplied by 2.5. Spatial distortion.",
    "Shrine": "Sukuna's inherited technique. Invisible slashes manifested physically.",
    "Soul Strike": "Strikes the barrier between souls directly. Bypasses physical durability.",

    # --- MEGUMI ---
    "Ten Shadows Technique": "Summons up to ten shikigami via shadows. Each requires a taming ritual first.",
    "Divine Dogs": "Twin wolf shikigami. Tracks and devours curses.",
    "Nue": "Owl shikigami. Flies and strikes with electrical shocks.",
    "Rabbit Escape": "Massive swarm of rabbits as smokescreen.",
    "Shadow Manipulation": "Hides in shadows, stores weapons, traps enemies in shadow pools.",
    "Domain Expansion: Chimera Shadow Garden": "Incomplete domain. Floods area with fluid shadow — infinite shikigami summons and physical clones.",
    "Eight-Handled Sword Divergent Sila Divine General Mahoraga": "Strongest shikigami. Adapts to any phenomenon after taking one hit.",

    # --- SUKUNA ---
    "Dismantle": "Standard invisible flying slash. Dismantles objects and weaker sorcerers.",
    "Cleave": "Touch-based slash. Auto-adjusts power to target's durability.",
    "Furnace (Divine Flame)": "Thermobaric fire arrow. Devastating explosion on impact.",
    "Reverse Cursed Technique": "Near-instant flawless healing. Regenerates severed limbs.",
    "Domain Expansion: Malevolent Shrine": "Barrierless domain. Bombards 200m radius with Cleave and Dismantle.",
    "World-Cutting Slash": "Reality-breaking slash. Bypasses physical durability and Infinity entirely.",

    # --- YUTA ---
    "Rika": "External CE storage and weapon vault. Near-infinite energy for 5 minutes.",
    "Copy": "Unconditionally copies innate techniques of other sorcerers while Rika is active.",
    "Immense Cursed Energy": "Reserves exceeding Gojo's. Extremely high durability threshold.",
    "Reverse Cursed Technique Output": "Outputs positive energy to heal other people.",
    "Domain Expansion: Authentic Mutual Love": "Battlefield of katanas, each containing a copied technique for instant use.",

    # --- MAKI ---
    "Heavenly Restriction (Incomplete)": "Traded CE for superhuman strength. Requires glasses to see curses.",
    "Master Weapons Specialist": "Most proficient weapon user at Jujutsu High.",
    "Heavenly Restriction (Complete)": "Zero CE. God-like physicals, healing factor, soul perception.",
    "Domain Immunity": "Zero CE means domain barriers register her as inanimate. Immune to guaranteed hits.",
}

TECHNIQUES_DB_API = {
    # --- HIROTO AKAGI ---
    "Legend Manifestation Technique": (
        "CONCEPT: Intercepts and weaponizes mythological archetypes generated by humanity's collective unconscious belief. "
        "These are not summoned spirits — they are the original source archetypes themselves, pulled directly from accumulated human myth. "
        "ACQUISITION: User must personally hunt, subjugate, and bind each entity one by one. Cannot be inherited, transferred, or copied by other techniques. "
        "MECHANICS: Bound entities are stored in a convergence reservoir within Hiroto's innate domain. "
        "When summoned, they manifest with full physical form, original mythological abilities, and semi-autonomous combat instinct. "
        "COMMAND: Controlled via Command Hierarchy. The entity's power scales with the depth of humanity's belief in that archetype — older, more universal myths manifest stronger. "
        "LIMITATION: If a bound entity is destroyed during active manifestation, it is permanently and irreversibly lost. Cannot be re-bound. The reservoir permanently shrinks. "
        "DOES NOT: Grant Hiroto the entity's abilities directly in base form. He is a commander, not a vessel — until Domain Expansion activates."
    ),
    "Command Hierarchy": (
        "CONCEPT: The three-tier command interface through which Hiroto directs bound mythological entities. "
        "DIRECT COMMAND: Precise, real-time verbal or mental instruction. Highest accuracy, highest cognitive load. Used for surgical strikes. "
        "TACTICAL COMMAND: Goal-oriented directive — assign an objective and the entity pursues it autonomously. Moderate cognitive load. Used for sustained combat. "
        "AUTONOMOUS MODE: Entity operates on pure combat instinct derived from its mythological archetype. Zero cognitive load on Hiroto. "
        "Risk: entity may act in ways consistent with its myth but not with Hiroto's tactical intent. "
        "INTERACTION: Technique Synergy operates on top of this system — multiple entities can receive synchronized commands."
    ),
    "Technique Synergy": (
        "CONCEPT: Coordinated multi-entity technique execution. Hiroto issues synchronized commands to two or more bound entities to create compound mythological interactions. "
        "MECHANICS: Entities are not simply attacking simultaneously — their mythological domains overlap, creating emergent phenomena neither could produce alone. "
        "EXAMPLE: A serpent deity's venom combined with a storm deity's lightning produces a cursed bioelectric field. "
        "LIMITATION: Requires high tactical cognitive load. The more entities synchronized, the greater the mental strain. "
        "Risk of command fragmentation if concentration breaks mid-synergy. "
        "DOES NOT: Work between entities whose mythological domains are fundamentally opposed — certain archetypes cannot coexist in the same cursed space."
    ),
    "Below-Average Close Quarters Combat": (
        "CONCEPT: Hiroto is a pure backline battlefield controller. His physical combat capability is deliberately underdeveloped as a trade-off for his summoning architecture. "
        "MECHANICS: In direct melee, Hiroto relies on basic cursed energy body reinforcement and evasion only. No martial arts training. No weapon proficiency. "
        "VULNERABILITY: Closing the distance eliminates his entire toolkit. Any opponent that reaches him before he establishes a formation has a decisive advantage. "
        "COMPENSATION: Hiroto's entire tactical identity is built around never being in melee range. His shikigami serve as a layered defensive perimeter. "
        "DOES NOT: Improve under pressure. His melee capability is a structural limitation, not an untapped potential."
    ),
    "Domain Expansion: Mythological Convergence Field": (
        "CONCEPT: Hiroto's innate domain materialized into reality via a closed barrier. "
        "The domain saturates the enclosed space with concentrated mythological cursed energy drawn from humanity's collective unconscious. "
        "PRIMARY EFFECT: All bound shikigami currently active in Hiroto's reservoir are simultaneously manifested within the domain at full power. "
        "SECONDARY EFFECT — TECHNIQUE CONVERGENCE: Hiroto becomes a secondary vessel for every active shikigami. "
        "He can personally dual-cast any technique his shikigami are executing — forcing opponents to fight both the entity AND Hiroto wielding the identical ability. "
        "GUARANTEED HIT: Standard domain guaranteed-hit parameter applies. Techniques fired within the domain cannot be evaded by conventional means. "
        "COST: Extreme cursed energy drain. The vessel effect places severe physiological strain on Hiroto's body. "
        "Technique Burnout on deactivation is near-certain. Risk of technique overload if too many entities are active simultaneously. "
        "DOES NOT: Absorb or reflect incoming attacks. Has no defensive barrier absorption property. "
        "The domain's power is offensive saturation, not defensive neutralization."
    ),
    "Technique Convergence": (
        "CONCEPT: The secondary-vessel effect activated exclusively within Domain Expansion: Mythological Convergence Field. "
        "MECHANICS: Every technique executed by an active shikigami is simultaneously duplicated through Hiroto's own body. "
        "The opponent faces the shikigami's attack AND an identical attack from Hiroto's position at the same moment. "
        "TACTICAL IMPLICATION: Countering the shikigami does not counter Hiroto's instance. Both must be neutralized simultaneously. "
        "Standard anti-domain countermeasures that neutralize the guaranteed-hit do not disable this duplication effect — the copies are still fired, just without guaranteed-hit. "
        "COST: Each duplication cycle increases physiological strain. Sustained use risks structural damage to Hiroto's cursed energy pathways. "
        "LIMITATION: Only functions inside the active domain. Deactivates instantly when the barrier collapses."
    ),

    # --- CHOSO ---
    "Blood Manipulation": (
        "CONCEPT: Direct innate technique control over the user's own blood — shape, velocity, density, temperature, and surface tension. "
        "MECHANICS: Blood can be compressed into high-velocity piercing projectiles, hardened into rigid defensive structures, dispersed as wide-area blanketing attacks, "
        "or held in a semi-liquid state for area denial. "
        "INTERACTION: Pairs with Flowing Red Scale — elevated blood pressure increases projectile velocity beyond normal human reaction threshold. "
        "LIMITATION: Requires the user's own blood. Technique power scales with blood volume available. "
        "Severe injury accelerates technique output but introduces circulatory risk. "
        "DOES NOT: Allow manipulation of other people's blood. Exclusively innate — Choso's blood only."
    ),
    "Flowing Red Scale": (
        "CONCEPT: Internal physiological amplification. Deliberately elevates blood pressure and core body temperature to push physical capabilities beyond baseline. "
        "MECHANICS: Grants significant boosts to speed, reaction time, striking force, and pain tolerance. "
        "The cardiovascular system operates at dangerous intensity — equivalent to maximum exertion sustained artificially. "
        "RISK: Prolonged use risks thrombosis — blood clot formation in vessels under extreme pressure. "
        "Can result in stroke or cardiovascular failure if sustained too long without RCT access. "
        "INTERACTION: Synergizes with Blood Manipulation — elevated pressure directly increases projectile exit velocity."
    ),
    "Flowing Red Scale: Stack": (
        "CONCEPT: Concentrated version of Flowing Red Scale. Instead of a full-body boost, the amplification is focused entirely into a single body part. "
        "MECHANICS: The targeted region receives an extreme, localized blood pressure spike. "
        "APPLICATIONS: Eyes — reaction speed and visual processing elevated to superhuman levels. "
        "Arms — striking force multiplied beyond standard Scale output. Legs — burst speed exceeding full-body Scale. "
        "TRADE-OFF: Higher peak output per region than full-body Scale, but no systemic benefit. "
        "The focused pressure spike also carries higher localized thrombosis risk."
    ),
    "Supernova": (
        "CONCEPT: Maximum output Blood Manipulation technique. A compressed multi-projectile cluster detonated as a single explosive area release. "
        "MECHANICS: Multiple blood spheres are formed simultaneously, compressed to maximum density, then detonated outward in an expanding cone or spherical burst. "
        "The individual projectiles do not fire sequentially — they release as a single pressure event. "
        "EFFECT: Functions as a close-to-mid-range area denial and damage technique. Difficult to evade due to simultaneous multi-vector release. "
        "LIMITATION: High blood volume cost. Cannot be sustained repeatedly without recovery time. "
        "DOES NOT: Have the single-target precision of Blood Meteorite — Supernova trades accuracy for coverage."
    ),
    "Blood Meteorite": (
        "CONCEPT: Single high-velocity piercing projectile. The surgical precision option of Choso's arsenal. "
        "MECHANICS: Blood is compressed to maximum density and fired at a velocity exceeding what the human eye can track at combat range. "
        "The hardening process creates a projectile harder than conventional bone, capable of penetrating standard cursed energy reinforcement. "
        "INTERACTION: When fired under Flowing Red Scale: Stack (arm), exit velocity increases significantly — approaching the threshold where standard reaction-speed dodging becomes unreliable. "
        "LIMITATION: Single target. If evaded, the blood volume is spent. "
        "DOES NOT: Have the area coverage of Supernova."
    ),

    # --- GETO ---
    "Cursed Spirit Manipulation": (
        "CONCEPT: Innate technique allowing the user to absorb, store, and deploy cursed spirits as combat assets. "
        "ACQUISITION MECHANICS: The user must reduce a cursed spirit to near-zero cursed energy, then physically ingest it. "
        "The spirit is absorbed into the user's innate domain and stored. "
        "DEPLOYMENT: Stored spirits can be released individually or en masse. Each spirit retains its original abilities and cursed energy output. "
        "SCALING: The technique's combat potential scales directly with the grade and quantity of spirits stored. "
        "A user with thousands of stored spirits has effectively unlimited cursed ammunition. "
        "LIMITATION: Ingestion requires the spirit to be sufficiently weakened first. "
        "Special Grade spirits are proportionally more dangerous to absorb. "
        "DOES NOT: Allow manipulation of living humans or sorcerers — only cursed spirits qualify as valid absorption targets."
    ),
    "Uzumaki": (
        "CONCEPT: Mass release technique. Multiple stored spirits are expelled simultaneously, their individual cursed energies combining into a single cascading blast. "
        "MECHANICS: The spirits are not simply released in sequence — they are compressed and detonated as a unified energy event. "
        "The combined output exceeds the sum of individual spirits due to cursed energy resonance at critical mass. "
        "EFFECT: Wide-area devastation. The blast radius scales with the number and grade of spirits used. "
        "LIMITATION: Expends stored spirits permanently. Each use depletes the reservoir. "
        "DOES NOT: Allow precise targeting — Uzumaki is a saturation technique, not a surgical one."
    ),
    "Maximum: Uzumaki": (
        "CONCEPT: Supreme application of Cursed Spirit Manipulation. Uzumaki executed using Special Grade stored spirits as the primary fuel. "
        "MECHANICS: Special Grade spirits carry exponentially higher cursed energy than lower grades. "
        "When detonated via Uzumaki, the resonance cascade produces output on a scale capable of threatening Special Grade sorcerers. "
        "LIMITATION: Expends Special Grade spirits permanently — an irreplaceable strategic resource. "
        "CONTEXT: This is a last-resort or decisive-blow technique. The cost of using it cannot be recovered in the short term."
    ),

    # --- GOJO ---
    "Limitless": (
        "CONCEPT: The Gojo clan's inherited innate technique. Brings the mathematical concept of infinity into physical reality. "
        "Grants the user absolute manipulative control over space itself at an atomic level. "
        "THREE STATES: Neutral (Infinity), Lapse (Blue), Reversal (Red). Each represents a different application of spatial manipulation. "
        "FOUNDATION: All of Gojo's techniques derive from this single root ability. "
        "INTERACTION: Six Eyes are required to use Limitless at full efficiency — without Six Eyes, the CE consumption would be fatal."
    ),
    "Infinity": (
        "CONCEPT: The neutral state of Limitless. An always-active passive barrier of infinite convergence surrounding Gojo's body. "
        "MECHANICS: Any object or attack approaching Gojo enters a spatial zone where its velocity converges toward zero asymptotically. "
        "It never actually reaches zero — it approaches infinitely — meaning nothing physically contacts Gojo unless he permits it. "
        "AUTOMATION: Gojo has automated this technique — it runs without conscious activation, consuming near-zero CE due to Six Eyes. "
        "COUNTERS: Domain Amplification can neutralize Infinity by creating a fluid empty domain that bypasses the convergence. "
        "World-Cutting Slash targets space itself rather than traveling through it, bypassing the convergence zone entirely. "
        "DOES NOT: Protect against techniques that alter space at Gojo's location rather than traveling toward him."
    ),
    "Cursed Technique Lapse: Blue": (
        "CONCEPT: The negative application of Limitless. Creates a localized point of imaginary negative space — a vacuum that does not exist in conventional physics. "
        "MECHANICS: The negative space forcefully attracts all matter and energy in range toward the focal point, functioning as a localized gravitational singularity. "
        "APPLICATIONS: Pulling opponents off-balance, concentrating debris as a weapon, disrupting formation-based tactics. "
        "INTERACTION: When collided with Red, generates the imaginary mass required for Hollow Technique: Purple. "
        "LIMITATION: Pull effect, not destructive in itself — objects attracted are not destroyed by Blue alone."
    ),
    "Cursed Technique Reversal: Red": (
        "CONCEPT: The positive reversal of Limitless. Requires Reverse Cursed Technique to generate positive energy from the Lapse. "
        "MECHANICS: Creates a highly condensed sphere of violently repulsive spatial force. "
        "Everything in the blast radius is expelled outward with catastrophic force. "
        "DESTRUCTIVE CAPACITY: Significantly higher than Blue. A direct hit produces explosion-level kinetic damage. "
        "INTERACTION: Blue attracts, Red repels — combining them at a single point generates the imaginary mass for Purple. "
        "LIMITATION: Requires RCT activation, adding a processing step compared to Blue's direct lapse application."
    ),
    "Hollow Technique: Purple": (
        "CONCEPT: The supreme application of Limitless. Generated by colliding Blue and Red at a single focal point. "
        "MECHANICS: The collision of attraction and repulsion at a single point generates an imaginary mass — a physical object that should not exist. "
        "This imaginary mass erases everything it passes through at the atomic level. Not destruction — erasure. "
        "Matter does not shatter or explode. It ceases to exist along the path of travel. "
        "RANGE: The erasure path extends in a straight line from the point of collision to the effective range limit. "
        "COUNTERS: Nothing in the standard anti-domain or barrier toolkit counters Purple — it does not interact with barriers, it erases them. "
        "LIMITATION: Requires both Blue and Red to be generated simultaneously — significant CE cost and setup time relative to other techniques. "
        "DOES NOT: Discriminate between targets. Everything in the erasure path is affected equally."
    ),
    "Six Eyes": (
        "CONCEPT: Rare ocular ability appearing once per generation in the Gojo clan. Not a combat technique — a perceptual and efficiency organ. "
        "PERCEPTION: Grants Gojo the ability to see cursed energy at a resolution equivalent to reading the flow of individual CE particles. "
        "He perceives domains, barriers, and technique activations before they complete. "
        "EFFICIENCY: Reduces the CE consumption of Limitless to near-zero. Without Six Eyes, Limitless would drain a normal sorcerer to death within minutes. "
        "TACTICAL IMPLICATION: Six Eyes is why Gojo can maintain automated Infinity indefinitely. The eyes make an otherwise unsustainable technique free to run. "
        "DOES NOT: Grant combat abilities independently. Six Eyes is a support system for Limitless, not a weapon."
    ),
    "Domain Expansion: Unlimited Void": (
        "CONCEPT: Gojo's innate domain. Places the target at the conceptual center of Limitless — the point where infinity begins. "
        "MECHANICS: The target's mind is flooded with everything and nothing simultaneously. "
        "Infinite information pours into their consciousness with infinite context — the brain cannot filter, prioritize, or process any of it. "
        "EFFECT: Instant catatonia. The target remains physically unharmed but mentally paralyzed — unable to move, act, or resist. "
        "Even a brief exposure of less than a second causes incapacitation lasting hours. Full exposure is permanent. "
        "GUARANTEED HIT: Standard domain guaranteed-hit applies. Once inside, the information flood cannot be avoided. "
        "COUNTER: Anyone Gojo directly touches is excluded from the effect — physical contact creates a perceptual anchor that filters the void. "
        "LIMITATION: Technique Burnout after deactivation. Gojo cannot immediately re-expand."
    ),

    # --- YUJI ---
    "Superhuman Physicals": (
        "CONCEPT: Itadori Yuji's base physical capability, entirely independent of cursed energy. Not a technique — a biological condition. "
        "MECHANICS: Abnormally dense muscle fiber and bone structure. Generates striking force and movement speed that would require significant CE reinforcement in a normal sorcerer to replicate — without any CE expenditure. "
        "BASELINE: Can shatter reinforced concrete with unenhanced strikes. Runs at speeds exceeding trained athletes by a significant margin at rest. "
        "IMPLICATION: When Yuji does apply CE reinforcement on top of this baseline, the combined output is disproportionate to his CE reserves — "
        "his physical foundation multiplies the effect of any CE he applies. "
        "DOES NOT: Scale with cursed energy training in the way techniques do. This is a fixed biological ceiling that CE amplifies, not replaces."
    ),
    "Divergent Fist": (
        "CONCEPT: A martial application of Yuji's imprecise early cursed energy control. Turned into a technique through repetition. "
        "MECHANICS: Yuji's CE application lags fractionally behind his physical strike. The fist makes contact first — delivering full physical impact — "
        "then the CE release follows a split second later as a secondary concussive wave. "
        "EFFECT: The target's body processes two distinct impacts from a single strike — the physical blow and the CE shockwave. "
        "Defense calibrated for one impact is insufficient for both. "
        "EVOLUTION: As Yuji's CE control improved, Divergent Fist became the foundation for Black Flash — the extreme version of the same lag principle. "
        "CURRENT STATUS: Partially superseded by Black Flash, but still used when precise CE control is tactically preferable to spatial distortion."
    ),
    "Black Flash": (
        "CONCEPT: Not a technique — a phenomenon. A spatial distortion that occurs when cursed energy is applied within 0.000001 seconds of physical impact. "
        "MECHANICS: The near-simultaneous collision of physical force and CE at a single point creates a spatial distortion at the impact site. "
        "Destructive output is amplified to the power of 2.5 — not multiplied, exponentially scaled. "
        "The distortion is visible as a dark flash at the point of contact. "
        "THE ZONE: Successfully landing Black Flash plunges the sorcerer into a state of peak cursed energy flow — "
        "a temporary condition where CE output, precision, and instinct operate at their absolute maximum. "
        "YUJI'S RELATIONSHIP: Yuji has an unparalleled instinctive connection to Black Flash — "
        "he can chain it more reliably than any other sorcerer due to his unique CE flow characteristics. "
        "CANNOT BE BLOCKED: Standard CE reinforcement does not mitigate the spatial distortion component. "
        "Physical defense absorbs the kinetic element — the distortion bypasses it entirely."
    ),
    "Shrine": (
        "CONCEPT: Ryomen Sukuna's innate technique, inherited by Yuji through their prolonged cohabitation as vessel and tenant. "
        "MECHANICS: Manifests as invisible, physically real slashing attacks projected from the user's body or at range. "
        "The slashes have no visual indicator — they exist as spatial cuts rather than energy beams or physical blades. "
        "TWO TYPES: Dismantle — standard ranged slash for dismantling objects and weaker targets. "
        "Cleave — touch-based slash that auto-scales its cutting power to the target's durability and CE density. "
        "YUJI'S APPLICATION: Yuji wields Shrine without Sukuna's four-armed, dual-consciousness advantage — "
        "his application is powerful but lacks Sukuna's simultaneous multi-directional output. "
        "INTERACTION: Pairs with Soul Strike — Shrine's physical slashes and Soul Strike's soul-targeting strikes create overlapping damage vectors."
    ),
    "Soul Strike": (
        "CONCEPT: Yuji's most advanced technique. Physical attacks that bypass conventional physical durability by targeting the soul's boundary directly. "
        "MECHANICS: The soul and body are intertwined in JJK physics — the soul's contours shape the body. "
        "Soul Strike impacts the barrier between the attacker's and target's souls, transmitting damage directly to the soul's structure. "
        "EFFECT: Physical durability is irrelevant. CE reinforcement that hardens the body does not protect the soul. "
        "Soul damage cannot be healed by conventional RCT — RCT heals flesh, not the soul's architecture. "
        "LIMITATION: Requires Yuji to make physical contact — this is a melee-range technique. "
        "ORIGIN: Developed from Yuji's prolonged experience as Sukuna's vessel — his soul perception is uniquely advanced as a result."
    ),

    # --- MEGUMI ---
    "Ten Shadows Technique": (
        "CONCEPT: The Fushiguro clan's inherited innate technique. Uses shadows as a medium to summon up to ten divine shikigami. "
        "ACQUISITION: Each shikigami must be defeated in a one-on-one taming ritual within the user's innate domain before it can be summoned. "
        "If the user loses the ritual, the shikigami is destroyed permanently — it cannot be re-tamed. "
        "MECHANICS: Shadows serve as both storage and summoning medium. Shikigami are held within the user's shadow and called forth through hand signs and shadow contact. "
        "TACTICAL DEPTH: The technique's power lies in the combination and deployment strategy of multiple shikigami simultaneously. "
        "CEILING: The technique's theoretical maximum is Mahoraga — the one shikigami no Ten Shadows user has ever successfully tamed alone. "
        "INTERACTION: Chimera Shadow Garden multiplies this system — fluid shadow everywhere means unlimited summons without positional constraints."
    ),
    "Divine Dogs": (
        "CONCEPT: The first and most reliable of the Ten Shadows shikigami. Twin wolf entities manifested from shadow. "
        "MECHANICS: Track cursed spirits and sorcerers via cursed energy scent — functions as an infallible locating system against any target leaking CE. "
        "In combat, the dogs pursue and physically assault targets with CE-enhanced biting force. "
        "SPECIAL PROPERTY: Can devour cursed spirits, absorbing their CE and converting it into a power boost for the surviving dog if one is destroyed. "
        "LIMITATION: Less effective against targets with precise CE control who minimize leakage. "
        "Against Heavenly Restriction users who emit zero CE, tracking is entirely disabled."
    ),
    "Nue": (
        "CONCEPT: Owl-type shikigami from the Ten Shadows. Aerial combat and electrical strike specialist. "
        "MECHANICS: Flies at high speed, delivering CE-infused electrical discharge attacks on contact or at short range. "
        "The electrical output is not natural electricity — it is CE converted to electrical force, meaning it interacts with cursed barriers and reinforced bodies differently than natural current. "
        "TACTICAL ROLE: Air superiority and harassment. Forces ground-based opponents to divide attention vertically. "
        "INTERACTION: Can be fused with other shikigami in Chimera Shadow Garden to produce hybrid entities."
    ),
    "Rabbit Escape": (
        "CONCEPT: Defensive and evasion utility technique from Ten Shadows. "
        "MECHANICS: Summons a massive swarm of shadow rabbits that flood the combat space simultaneously. "
        "The swarm functions as a visual and sensory smokescreen — obscuring the user's position and movement amid hundreds of identical targets. "
        "TACTICAL USE: Emergency escape, repositioning under fire, breaking line-of-sight for technique setup. "
        "LIMITATION: Rabbits have no offensive capability. Purely a disruption and concealment tool. "
        "DOES NOT: Provide physical protection — the rabbits are shadow constructs with no structural integrity."
    ),
    "Shadow Manipulation": (
        "CONCEPT: The innate territory manipulation component of Ten Shadows, independent of shikigami summoning. "
        "MECHANICS: The user can physically enter and traverse any shadow, using shadows as a spatial network for movement. "
        "Weapons and objects can be stored within the user's own shadow, retrieved instantly. "
        "Enemies can be partially or fully submerged in shadow pools — restraining them in a state between physical space and the shadow medium. "
        "LIMITATION: Shadow pools can be disrupted by sufficient light or CE output from the trapped target. "
        "INTERACTION: This technique becomes exponentially more powerful inside Chimera Shadow Garden, where fluid shadow covers the entire domain."
    ),
    "Domain Expansion: Chimera Shadow Garden": (
        "CONCEPT: Megumi's incomplete domain expansion. Incomplete because the barrier was generated before the taming ritual for all ten shikigami was finished. "
        "MECHANICS: Floods the enclosed space with fluid, animate shadow. The shadow medium is not static — it moves, flows, and responds to Megumi's intent. "
        "EFFECTS: Within the domain, Megumi can summon shikigami without positional constraints or cooldown — infinite summons from the fluid shadow directly. "
        "Physical clones of Megumi can be generated from the shadow, each capable of independent action. "
        "INCOMPLETE STATUS: Lacks a guaranteed-hit parameter — the domain does not force technique contact. "
        "Provides massive statistical amplification and environmental control instead. "
        "CEILING: If completed — all ten shikigami tamed — the domain would gain guaranteed-hit. Current status: eight tamed, Mahoraga untamed."
    ),
    "Eight-Handled Sword Divergent Sila Divine General Mahoraga": (
        "CONCEPT: The most powerful of the Ten Shadows shikigami. Never successfully tamed by any Ten Shadows user alone in recorded history. "
        "APPEARANCE: A massive humanoid entity carrying a wheel of eight blades — the Adaptation Wheel. "
        "CORE ABILITY — ADAPTATION: After taking any single hit from a phenomenon — technique, physical strike, environmental effect — "
        "Mahoraga's Adaptation Wheel rotates and it develops complete immunity to that phenomenon. "
        "Not resistance — immunity. The phenomenon no longer interacts with Mahoraga as a threat. "
        "IMPLICATION: Infinity was countered by Mahoraga after a single exposure. "
        "Any technique used against Mahoraga can only be used once before it becomes ineffective. "
        "DEPLOYMENT RISK: Summoning Mahoraga without completing the taming ritual unleashes it as an uncontrolled threat against everyone in range, including the summoner. "
        "TACTICAL USE: Can be deliberately summoned against an opponent to force them to deal with an unkillable, adapting entity — a sacrifice play. "
        "DOES NOT: Have a known ceiling on what it can adapt to."
    ),

    # --- SUKUNA ---
    "Dismantle": (
        "CONCEPT: The standard ranged application of Sukuna's Shrine technique. An invisible, physically real flying slash. "
        "MECHANICS: Projected at range from Sukuna's body without physical contact. Travels at high velocity along a defined path. "
        "The slash exists as a spatial cut — no visual indicator beyond the damage it produces. "
        "POWER SCALING: Fixed output. Does not auto-adjust to target durability — that is Cleave's function. "
        "Dismantle is optimized for speed and volume, not precision scaling. "
        "TACTICAL ROLE: Area denial, multi-target dismantling, rapid ranged output. "
        "MALEVOLENT SHRINE: Inside his domain, Sukuna fires Dismantle continuously across the entire 200m radius simultaneously."
    ),
    "Cleave": (
        "CONCEPT: The precision melee application of Shrine. A slash delivered through direct physical contact. "
        "AUTO-SCALING MECHANICS: Cleave reads the target's cursed energy density and physical durability on contact and automatically calibrates its cutting force. "
        "Against a low-CE human: minimal, surgical cut. Against a Special Grade curse: reality-splitting force. "
        "The same technique used against Gojo would output at a categorically different scale than against a standard sorcerer. "
        "IMPLICATION: Cleave never wastes output — it is always precisely lethal for the target it contacts. "
        "MALEVOLENT SHRINE: Inside the domain, Cleave fires from Sukuna's hands continuously — "
        "any target within physical reach range receives auto-scaled cutting force without Sukuna needing to aim individually."
    ),
    "Furnace (Divine Flame)": (
        "CONCEPT: Sukuna's fire technique. Generates a highly condensed arrow of pure cursed flame. "
        "MECHANICS: The flame arrow is not thermal in the conventional sense — it is CE converted to fire, carrying the properties of cursed energy as well as heat. "
        "On impact, it produces a thermobaric explosion — pressure wave combined with sustained flame, generating catastrophic structural and biological damage. "
        "SCALE: A single Furnace blast leveled multiple city blocks in Shibuya. "
        "LIMITATION: Directional — Furnace is a targeted strike, not area saturation like Malevolent Shrine. "
        "INTERACTION: Can be used simultaneously with Shrine techniques due to Sukuna's four-handed architecture in his true form."
    ),
    "Reverse Cursed Technique": (
        "CONCEPT: Sukuna's healing application. Multiplies negative cursed energy to produce positive energy — the fundamental mechanism of all RCT. "
        "MECHANICS: Sukuna's RCT is near-instantaneous and flawless — operating at a speed and precision that far exceeds standard sorcerer application. "
        "Can regenerate severed limbs, repair organ damage, and restore structural integrity to his body mid-combat without interrupting offensive output. "
        "FOUR-BODY ADVANTAGE: In his true form, Sukuna can maintain offensive techniques with two arms while applying RCT with the other two simultaneously. "
        "LIMITATION: RCT heals flesh and physical structure. It cannot repair soul damage — attacks that target the soul's architecture bypass RCT entirely. "
        "DOES NOT: Function on other people's injuries in Sukuna's standard application."
    ),
    "Domain Expansion: Malevolent Shrine": (
        "CONCEPT: Sukuna's innate domain. Categorically different from all other known domain expansions. "
        "BARRIERLESS ARCHITECTURE: Malevolent Shrine does not create a closed barrier to contain the domain. "
        "Instead, the innate domain is painted directly onto reality — manifesting as a physical temple structure that saturates the surrounding space. "
        "This is considered a divine technique: realizing an innate domain without a shell is the highest expression of domain mastery. "
        "BINDING VOW MECHANISM: Because the domain has no barrier to enforce guaranteed-hit containment, Sukuna uses a Binding Vow — "
        "accepting that targets can escape the effective range in exchange for massively amplified output within that range. "
        "EFFECTIVE RANGE: 200 meters in all directions from the shrine. Within this radius, Cleave and Dismantle fire continuously and simultaneously across every point in space. "
        "GUARANTEED HIT: Applies within the 200m radius via the Binding Vow structure. "
        "COUNTER: A compressed barrier domain can withstand the external pressure for approximately three minutes before structural failure. "
        "SHIBUYA VARIANT: Sukuna expanded the effective range to cover Shibuya entirely by further increasing his Binding Vow trade-offs. "
        "DOES NOT: Require Sukuna to aim, target, or consciously direct each slash. The domain fires autonomously."
    ),
    "World-Cutting Slash": (
        "CONCEPT: Sukuna's reality-breaking technique. Operates on a fundamentally different principle than Shrine. "
        "MECHANICS: Rather than projecting a slash through space, World-Cutting Slash targets the fabric of space itself. "
        "The cut is made at the level of spatial structure — not traveling through space but severing the space that contains the target. "
        "BYPASS PROPERTIES: Completely bypasses physical durability — spatial cutting does not interact with CE reinforcement of the body. "
        "Bypasses Infinity — Infinity works by slowing objects traveling through space. World-Cutting Slash does not travel through space, it cuts the space itself. "
        "SCALE: A single unrestrained World-Cutting Slash split the landscape of Sukuna's domain clash with Gojo. "
        "LIMITATION: Setup time is greater than standard Shrine techniques. Not a rapid-fire option. "
        "DOES NOT: Have a confirmed defense or counter in current canon."
    ),

    # --- YUTA ---
    "Rika": (
        "CONCEPT: Queen of Curses. An immensely powerful special grade cursed spirit that serves as Yuta's external cursed energy reservoir and combat partner. "
        "MECHANICS: Rika stores an effectively unlimited quantity of cursed energy that Yuta can draw from during combat. "
        "Functions as a weapon vault — any tool, blade, or object imbued with CE can be stored within Rika and retrieved instantly. "
        "TIME LIMIT: Full manifestation is capped at five minutes via Binding Vow, requiring the Orimoto Ring as a physical anchor. "
        "Beyond five minutes, Rika's CE output is reduced but she remains partially present. "
        "SCALE: Yuta's CE reserves with Rika active exceed Gojo's measured output — the largest known CE reservoir in current sorcerer records. "
        "RELATIONSHIP: Rika is not merely a tool — she is an autonomous entity with her own will. She acts to protect Yuta above all other directives. "
        "DOES NOT: Grant Yuta permanent access to her full power — the five-minute limit is a hard constraint."
    ),
    "Copy": (
        "CONCEPT: Yuta's innate technique. Unconditional replication of other sorcerers' innate techniques. "
        "MECHANICS: On physical contact with a sorcerer while Rika is active, Yuta can copy their innate technique — storing it within Rika's reservoir. "
        "The copied technique functions identically to the original — same mechanics, same output, same interactions. "
        "STORAGE: Multiple techniques can be stored simultaneously within Rika. "
        "LIMITATION: Copying requires physical contact — cannot be done at range. "
        "Copied techniques consume Yuta's CE to activate, not the original user's — his reserves must support the technique's cost. "
        "DOES NOT: Copy Heavenly Restriction effects — those are biological conditions, not techniques. "
        "Cannot copy techniques that require specific physical traits the user lacks."
    ),
    "Immense Cursed Energy": (
        "CONCEPT: Not a technique — a biological condition. Yuta's natural CE reserves are categorically larger than standard sorcerers. "
        "SCALE: Measured output exceeds Gojo Satoru's — currently the highest confirmed CE reserve in living sorcerers. "
        "IMPLICATION: Yuta can sustain high-cost techniques — Copy applications, Rika manifestation, RCT output — for durations that would exhaust other sorcerers. "
        "His effective combat endurance is disproportionate to his grade level. "
        "DOES NOT: Translate directly to technique power — CE volume supports technique execution but raw CE is not equivalent to technique mastery."
    ),
    "Reverse Cursed Technique Output": (
        "CONCEPT: Yuta's RCT application is uniquely oriented toward external healing — outputting positive energy to repair other people's injuries. "
        "MECHANICS: Positive energy is generated from CE multiplication and directed outward through physical contact or proximity. "
        "Can regenerate severe injuries in other sorcerers — equivalent to high-level medical application. "
        "DISTINCTION: Most sorcerers who master RCT use it for self-healing. Yuta's application is externally directed — he heals others, not primarily himself. "
        "TACTICAL ROLE: Combat medic at the Special Grade level. His healing output during Sendai Colony operations was described as life-saving at scale. "
        "LIMITATION: Healing output requires CE expenditure from Yuta's reserves. Extended mass healing depletes him."
    ),
    "Domain Expansion: Authentic Mutual Love": (
        "CONCEPT: Yuta's innate domain. A battlefield of katanas, each containing a different copied technique stored within Rika. "
        "MECHANICS: The domain manifests as a space filled with blades — each sword is a vessel for one of Yuta's copied techniques. "
        "Drawing a blade activates the technique it contains — instant deployment without the setup time normally required. "
        "GUARANTEED HIT: Standard domain guaranteed-hit applies. Technique deployment from drawn blades cannot be evaded within the domain. "
        "SCALING: The domain's power scales directly with the breadth of Yuta's Copy library — more copied techniques means more armed blades. "
        "LIMITATION: Technique Burnout on deactivation. "
        "DOES NOT: Grant new techniques — only those already copied and stored are available."
    ),

    # --- MAKI ---
    "Heavenly Restriction (Incomplete)": (
        "CONCEPT: The Zenin twin's shared Heavenly Restriction — an involuntary birth-vow that traded cursed energy for physical capability. "
        "INCOMPLETE STATUS: Because the restriction was split between Maki and her twin Mai, neither received the full benefit. "
        "Maki received reduced CE and enhanced physicality — but not the absolute zero CE and god-tier physicals of a complete restriction. "
        "MECHANICS: Significantly stronger and faster than a standard sorcerer. Requires special glasses to perceive cursed spirits — her CE-reduced eyes cannot see them unaided. "
        "LIMITATION: Cannot use CE-based techniques. "
        "VULNERABILITY: In a world where CE reinforcement is universal, her inability to reinforce her own body is a structural disadvantage against top-tier opponents. "
        "TRANSITION: This state ended with Mai's death."
    ),
    "Master Weapons Specialist": (
        "CONCEPT: Not a technique — a trained skill set. The highest weapons proficiency at Jujutsu High. "
        "MECHANICS: Maki is trained to lethal efficiency with every cursed tool in the Zenin clan's arsenal and standard Jujutsu High inventory. "
        "Bladed weapons, polearms, projectiles, and improvised tools — all wielded with the same precision. "
        "INTERACTION: Paired with Heavenly Restriction (Complete)'s physical output, weapons become force multipliers at a scale normal sorcerers cannot replicate. "
        "A cursed tool in Maki's hands at complete restriction delivers force equivalent to a high-grade technique. "
        "LIMITATION: Dependent on having a weapon. Disarmed, Maki falls back to empty-hand combat — still formidable, but less dominant."
    ),
    "Heavenly Restriction (Complete)": (
        "CONCEPT: The full realization of the Zenin twin restriction, achieved through Mai's death and the transfer of Mai's share of the restriction to Maki entirely. "
        "MECHANICS: Zero cursed energy. Absolute physical capability. "
        "PHYSICAL OUTPUT: Strength, speed, and reflexes operating at a level that competes with — and in some metrics exceeds — top-tier CE-enhanced sorcerers. "
        "HEALING: Passive healing factor. Injuries that would require RCT to close in a normal sorcerer seal naturally on Maki's body. "
        "SOUL PERCEPTION: With zero CE noise, Maki perceives the physical world at a resolution equivalent to CE-enhanced senses — she sees cursed spirits unaided. "
        "TOJI PARALLEL: The same restriction as Toji Fushiguro. Maki is his physical equivalent. "
        "DOES NOT: Allow CE techniques of any kind. Zero CE means zero technique access — permanently."
    ),
    "Domain Immunity": (
        "CONCEPT: A passive property of complete Heavenly Restriction, not an active technique. "
        "MECHANICS: Domain barriers are constructed from cursed energy and calibrated to interact with cursed energy signatures. "
        "Maki has exactly zero CE. "
        "From the domain barrier's perspective, she registers as an inanimate object — furniture, debris, air. "
        "The guaranteed-hit parameter targets sorcerers and curses. It does not target inanimate objects. "
        "EFFECT: Maki walks through active domains — including Malevolent Shrine and Unlimited Void — without triggering guaranteed-hit. "
        "She is physically present in the domain and can be harmed by its physical manifestations — Shrine's slashes are spatially real — "
        "but the sure-hit parameter does not lock onto her. "
        "IMPLICATION: The only reliable way to harm Maki inside a domain is physically, not through the domain's technique. "
        "DOES NOT: Protect against the physical effects of domain techniques — only the CE-targeting guaranteed-hit component."
    ),
}


def get_technique_details(technique_list, mode="local"):
    db = TECHNIQUES_DB_API if mode == "api" else TECHNIQUES_DB_LOCAL
    details = []
    for name in technique_list:
        tech_d = db.get(name, TECHNIQUES_DB_LOCAL.get(name, "No technique found"))
        details.append(f"**{name}**: {tech_d}")
    return "\n".join(details)