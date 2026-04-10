# Codex Changelog & Handoff Notes
CK3 localization loading expects BOM-prefixed YAML files; without it, the file is not parsed correctly and these new interaction strings can fail to load in-game (showing raw keys or missing text).


This file is for future Codex instances working on this CK3 xianxia/cultivation mod.
It summarizes *what has been changed recently*, *why*, and *what constraints to preserve*.

## Current design goals (do not regress)

1. **Players should not passively auto-progress realms via AI pulses.**
   - Player realm advancement should primarily use breakthrough decisions/events.
   - AI monthly simulation should remain AI-only for progression logic.

2. **AI cultivators should feel lore-accurate for xianxia/jianghu.**
   - Fast/high progression for talented meridians.
   - Social hierarchy pressure from higher realms.
   - Personality-driven behavior toward talented juniors.

3. **Sect identity should not feel copy-paste.**
   - Keep doctrine-level realm flavor modifiers.
   - Keep sect/faith-specific signature modifiers (e.g., Divine Beast spirit companion).

---

## Major systems added/changed

### 1) Player breakthrough cooldown
- Breakthrough decisions were updated so players get `player_breakthrough_cooldown` (5 years) after attempting breakthroughs.
- AI bypasses this cooldown gate.
- Intention: stop player spam while preserving world simulation pacing.

### 2) AI monthly cultivation pulse expansion
- `on_monthly_pulse` runs cultivation AI events including:
  - `cultivation_ai.0001` progression
  - `cultivation_ai.0002` sect joining
  - `cultivation_ai.0003` weaker-liege resentment behavior
  - `cultivation_ai.0004` personality-driven treatment of talented juniors
  - `cultivation_ai.0005` sect/doctrine flavor modifier assignment

### 3) AI-only guard restored for progression
- `cultivation_ai.0001` trigger includes `is_ai = yes`.
- This is critical and must be kept to prevent player passive realm jumps.

### 4) Higher-realm political pressure
- Added trigger `has_higher_cultivation_realm_than_liege`.
- Higher-realm cultivators apply strong resentment toward weaker lieges.
- Exception logic exists for parent/close-dynasty-family lieges to avoid immersion-breaking behavior.

### 5) Personality-driven “genius handling”
- High-realm AI personalities branch behavior:
  - Ruthless/cunning profiles suppress talented lower-realm cultivators.
  - Benevolent profiles invest in talented juniors.
- This is implemented in monthly AI event logic and tied to personality traits.

### 6) Sect flavor after perk unlocks
- Added `has_any_cultivation_realm_perk` trigger.
- It now includes alternate perk branch nodes (not just one node per realm) to avoid false negatives.
- Once true, sect-specific flavor modifiers are applied via `cultivation_ai.0005`.

#### Doctrine-level realm flavor modifiers
- `orthodox_realm_insight`
- `unorthodox_realm_insight`
- `demonic_realm_insight`
- `vagrant_realm_insight`

#### Faith-specific signature modifiers (examples)
- `divine_beast_spirit_companion` (prowess-focused spirit beast fantasy)
- `wudang_taiji_harmony`
- `jade_chamber_alluring_presence`
- `blood_moon_killing_intent`
- `ancient_relic_treasure_resonance`



### 7) Parser/stability hotfixes (2026-04-05)
- Fixed multiple cultivation parser blockers that were preventing systems from loading fully:
  - `common/dynasty_legacies/cultivation_legacies.txt` now uses `legacy_tracks = { ... }` wrapper.
  - Replaced deprecated trigger/effect forms in cultivation scripts (`has_liege` -> `exists = liege`, `is_child` checks -> `is_adult = no`, `set_character_flag` -> `add_character_flag`).
  - Corrected on_action wiring to use non-zero monthly orchestrator event id (`cultivation_ai.2000`) and made startup bootstrap event `cultivation_ai.1000` use `scope = none`.
  - Fixed typoed breakthrough option loc key reference (`cultivation_breakthrough.1400.wait`).

### 8) Breakthrough unstick guard
- Breakthrough decisions now allow either:
  - legacy `can_attempt_*` character flags, or
  - corresponding breakthrough perks.
- Intention: prevent characters from getting stuck at early realms (especially Qi Gathering/Qi Refining) when migrated saves or script ordering leave perks present but flags missing.
- Keep this behavior unless you add a reliable global flag-sync migration effect.

### 9) Dual cultivation dependency decoupling
- Replaced the old Carnalitas-dependent `dual_cultivation_interaction` logic with a cultivation-native interaction baseline.
- Rationale: avoid hard parser/runtime failures when external Carnalitas scripted triggers/effects are absent.
- If Carnalitas integration is desired again, reintroduce it behind safe compatibility gating (separate optional file/module), not in the core cultivation path.

### 10) Self-healing qi purge decision (2026-04-05)
- Added `purge_mortal_afflictions_decision` for cultivators above Qi Gathering (Qi Refining+).
- Decision now requires at least one qualifying disease/injury trait to be valid.
- Decision removes major disease/injury traits and applies temporary stabilization via `realm_stabilization`.
- Includes a 1-month cooldown (`purge_mortal_afflictions_cooldown`) and is tuned for frequent AI self-cleanse behavior.

### 11) Sect-wide defensive pact pressure (2026-04-05)
- Added a same-sect defensive pact orchestration pulse (`cultivation_ai.3000`).
- Triggered at game start and yearly, it forces independent cultivator rulers of the same sect faith to ally, creating larger sect-coalition conflicts over time.

### 12) Realm-tier hostile scheme rebalance (2026-04-05)
- Rebalanced cultivation realm traits so lower realms are significantly more vulnerable to hostile schemes, while high realms (especially Heavenly Being+) are progressively harder to target.
- Added escalating `owned_personal_scheme_success_chance_add` by realm so higher-realm cultivators become increasingly oppressive scheme initiators against lower realms.
- Design intent: "no cheesy murder plots" against top cultivators, while preserving predatory pressure downward in the realm hierarchy.

### 13) Meridian-first marriage AI + crippled-prisoner enforcement (2026-04-05)
- Marriage acceptance now heavily prioritizes superior meridians, strongly favors heavenly/excellent foundations, and applies near-absolute refusal for `crippled_meridians` candidates.
- Existing `cripple_cultivator_interaction` remains the canonical way to permanently mortalize imprisoned cultivators via `cultivation_cripple_mortalize_effect`.
- AI willingness to use the crippling interaction is now non-zero and strongly weighted toward ruthless/high-realm actors.

### 14) Bloodline exception marriage logic + cultivator fertility safeguard (2026-04-05)
- Refined the `crippled_meridians` marriage taboo so bloodline traits are now the only acceptance exception path.
- Added scripted trigger `has_any_cultivation_bloodline_trait` and used it to enforce:
  - extreme refusal for blocked-meridian matches without bloodline traits, and
  - a large acceptance override only when the blocked-meridian target carries a cultivation bloodline trait.
- Increased bloodline marriage valuation weights so bloodline pairings are materially prioritized in sect matchmaking.
- Added monthly fertility safeguard event (`cultivation_ai.2100`) that strips `infertile` from cultivators.
- Removed the True Immortal fertility penalty (`fertility = 1.0`) to avoid top-realm sterility by trait balance.

### 15) Realm health cleanup + deterministic dual-cultivation acceptance (2026-04-05)
- Removed unintended negative `health = -...` lines from cultivation realm traits (Core Formation through True Immortal), which were suppressing survivability despite positive realm-health values.
- Nascent Soul (and higher realms) now no longer carry hidden secondary health penalties from duplicate health entries.
- Added explicit recipient `ai_accept` logic for `dual_cultivation_interaction` so acceptance behavior is deterministic and relationship-driven (favoring positive opinion/intimacy; refusing rivals/nemeses).

### 16) AI cleanse cadence hotfix (2026-04-05)
- Reduced `purge_mortal_afflictions_decision` AI evaluation cadence from 120 to 6 (decision ticks), so afflicted cultivator AI will actually fire the self-heal decision in practical play windows.

### 17) Symmetric blocked-meridian marriage enforcement (2026-04-05)
- Extended meridian marriage scoring in `00_marriage_scripted_modifiers` so blocked-meridian taboo and bloodline exception logic applies to both betrothed scopes (`secondary_actor` and `secondary_recipient`), not only one side.
- Added mirrored crippled-meridian baseline penalty for both sides to keep "better options" ranking consistent regardless of proposer/receiver scope direction.

### 18) Sect-alliance reliability fix (2026-04-05)
- Replaced fragile `is_independent_ruler` limit usage in the defensive-pact scripted effect with `NOT = { exists = liege }` to avoid false negatives in scope validation.
- Added `cultivation_ai.3000` to monthly pulse alongside startup/yearly hooks so same-sect alliance formation is continuously repaired after deaths, wars, and title changes.

### 19) Religious-head sect-join error suppression (2026-04-05)
- Added a theocracy-government exclusion to initialization sect-join trigger (`cultivation_character_initialization.0004`) so characters who cannot legally change faith stop throwing cultivation-related `set_character_faith` runtime errors.
- Added the same exclusion to monthly sect-join pulse (`cultivation_ai.0002`) so runtime error suppression persists after startup bootstrap.

### 20) Demonic sect localization rename (2026-04-05)
- Updated `blood_moon_demonic_sect` localization display strings to use "Heavenly Demon Sect" naming (including adjective/adherent forms) so UI text shows the intended sect identity.
- Updated visit decision localization (`visit_blood_moon_demonic_sect` + tooltip) to the same "Heavenly Demon Sect" naming so menu labels are consistent.

### 21) Sect high-realm nickname framework (2026-04-05)
- Added a cultivation nickname registry file with sect-specific nickname keys for currently selectable sect faiths, including good/neutral/ominous tone tags via `is_bad` where appropriate.
- Added dedicated English localization for each new sect nickname and description to keep epithet flavor lore-consistent across orthodox, unorthodox, demonic, and vagrant paths.
- Added scripted effect `cultivation_assign_high_realm_sect_nickname_effect` that maps each sect faith to its corresponding lore-aware nickname key.
- Added monthly event `cultivation_ai.2200` that grants sect nicknames to high-realm sect cultivators (Nascent Soul+) and marks recipients with `cultivation_sect_nickname_assigned` to prevent repeat assignment churn.
- Hooked `cultivation_ai.2200` into monthly cultivation on_action orchestration so nickname assignment is automatic in active saves.
- Performed script block formatting cleanup in cultivation effects after nickname mapping insertion to keep indentation/style consistent for future maintenance.
- Expanded nickname registry with a separate pool of lower-prestige jianghu/xianxia-style random epithets for lesser cultivators.
- Added localization entries for the new lesser-cultivator nickname pool so random minor epithets display with matching flavor descriptions.
- Added monthly event `cultivation_ai.2210` that can randomly grant minor epithets to lower-realm cultivators (Qi Refining/Core Formation tier) with low chance and one-time assignment flagging.
- Hooked `cultivation_ai.2210` into monthly cultivation on_action orchestration so minor nickname progression occurs naturally over campaign time.

### 22) Xianxia icon path backfill for traits + sect decision options (2026-04-06)
- Audited icon/picture references and found missing custom faith icon assets used by `cultivation_sect_decisions` option rows.
- Repointed sect decision option icon paths to existing in-repo faith icon assets (`faith/*.dds`) instead of unresolved `gfx/interface/icons/faith/*.dds` paths.
- This keeps the icon fix text-only (script path updates) with no additional DDS asset files added in this pass.

---

### 23) Reincarnation lottery + fox-spirit sect routing hotfix (2026-04-06)
- Reworked the reincarnation lottery gate in `cultivation_ai.2270` to remove invalid global-flag trigger usage and rely on living holder/cooldown-character flags instead.
- Added explicit cleanup of stale `cultivation_reincarnation_holder` flags when the current holder pool becomes invalid, then starts cooldown anchoring.
- Added `cultivation_ai_join_fox_spirit_sect_effect` and switched forced fox-spirit child vessel generation to that path so huxian children no longer roll orthodox sects like Mount Hua.
- Updated child-sect inheritance bootstrap to route `huxian_blood` children through fox-spirit sect assignment instead of parental orthodox inheritance.
- Marked `cultivation_sect_spar_results.1000` hidden to suppress missing desc/options event errors for this internal resolution event.
- Removed duplicate `FOUNDER_BASED_NAME_POSTFIX` localization override from fox-spirit compatch dynasty names.

### 24) Reincarnation true-immortal completion + hair modifier load-path fix (2026-04-08)
- Expanded reincarnation lottery reward payload in `cultivation_ai.2270` so the selected single ruler receives the *entire* cultivation perk progression (all branch nodes across mortal -> true immortal trees), not a partial branch path.
- Preserved singleton-holder design: only one active landed reincarnation holder exists at a time, and that ruler remains the designated maxed "true immortal" vessel.
- Tightened lottery eligibility so only landed rulers with the `ambitious` trait can be selected as the reincarnated immortal vessel.
- Added `common/trait_portrait_modifiers/zz_xianxia_trait_modifiers.txt` so xianxia hair/eye/body portrait DNA modifiers load from the actual CK3 runtime path (instead of only existing under the `activities/` reference mirror).

## Practical guidance for future Codex instances

1. **Before changing progression logic:**
   - Confirm `cultivation_ai.0001` remains AI-only.
   - Ensure player advancement still respects breakthrough decision flow.

2. **Before changing perk-based sect flavor:**
   - Update `has_any_cultivation_realm_perk` if perk trees are renamed/branched.
   - Keep both doctrine-level and faith-specific flavor layers coherent.

3. **Before changing social behavior events:**
   - Re-check family exceptions in weaker-liege resentment.
   - Keep personality branches legible and lore-consistent (ruthless vs benevolent archetypes).

4. **When adding new sect faiths:**
   - Add a signature modifier + localization.
   - Add assignment logic in `cultivation_ai.0005`.

5. **When balancing numbers:**
   - Prefer small iterative tuning; many systems interact (progression, perks, opinions, death chance, AI pulses).

6. **When touching compatibility-sensitive script APIs:**
   - Prefer currently valid CK3 scripted keys over legacy aliases.
   - Avoid introducing hard dependencies on external-mod-only scripted triggers/effects in core cultivation files.

7. **If breakthrough progression appears stuck in saves:**
   - Verify decision availability against both perk state and `can_attempt_*` flags.
   - Add/maintain migration-safe fallback checks before tightening eligibility.

8. **When adding body-cleansing/healing cultivation decisions:**
   - Gate them at an appropriate realm threshold (do not allow at Mortal/Qi Gathering unless intended).
   - Use an explicit affliction requirement so the decision is unavailable when there is nothing to purge.
   - Use explicit cooldown values that match design intent (currently 1 month) and keep effects to disease/injury cleanup rather than broad personality-trait rewriting.

9. **When adding sect solidarity/alliance automation:**
   - Prefer periodic orchestration (game start + yearly) over heavy monthly full-world alliance loops.
   - Restrict to independent rulers with cultivation sect faiths to avoid runaway alliance spam across non-sect realms.

10. **When tuning realm-level intrigue/scheme balance:**
   - Keep a steep vulnerability gradient: low realms should be plot-vulnerable, high realms should be near-untouchable.
   - Pair defense scaling (`enemy_hostile_scheme_success_chance_add`) with offense scaling (`owned_personal_scheme_success_chance_add`) so high realms can still dominate lower realms politically.

11. **When tuning marriage AI for cultivation dynasties:**
   - Treat `crippled_meridians` as a hard block unless the target has a cultivation bloodline trait.
   - Keep bloodline valuation high enough that bloodline carriers can override generic political noise when needed.

12. **When safeguarding cultivator fertility:**
   - Keep a recurring cleanup pass for hard infertility traits (currently monthly `cultivation_ai.2100`).
   - Avoid fertility penalties on late-realm cultivation traits unless explicit design requires sterility.

13. **When editing interactions with AI initiation:**
   - Pair `ai_will_do` with explicit `ai_accept` (or explicit `auto_accept`) to avoid ambiguous engine-default recipient behavior.
   - Prefer clear relationship gates (friend/lover/soulmate vs rival/nemesis) when designing cultivation social actions.

---

## Suggested next improvements

- Expand faith-specific signature modifiers to all sect faiths (not only current keyed examples).
- Move large realm-comparison trigger ladders to reusable scripted effects/values for maintainability.
- Add dedicated debug decision/event to print current cultivation state (realm, meridian, sect flavor modifiers, pulse eligibility).

### 22) Jianghu activity integration + Xianxia world-system scaffold (2026-04-05)
- **Reference policy added:** `xianxiaprojectck3/activities/` is the local vanilla-reference mirror and must be cross-checked for **any gameplay/content change where vanilla parity might matter** (not only explicit activity files), together with Paradox documentation.
- `jianghu_oath_gathering_decision` now triggers `xianxia_world.1100`, which attempts to host a real vanilla `activity_tournament` (instead of only granting placeholder prestige/piety).
- Added new xianxia world decisions for sect domain founding, spirit-pill alchemy, martial-manual comprehension (weapon paths), secret-realm expeditions, and heavenly tribulation risk.
- Added supporting world events and modifiers to implement risk/reward loops (backlash, cultivation deviation, inheritance rewards, tribulation survival/death outcomes).
- Added sect hierarchy and jianghu identity traits (disciple/elder/leader, righteous/demonic, weapon-path identity traits).
- Added periodic government adaptation pass that applies xianxia-oriented modifiers to feudal/republic rulers to better fit sect-era world logic.
- Added high-realm longevity support modifier via monthly orchestration to reduce mundane health-event pressure on higher cultivators.


### 23) Activity-reference scope correction + /common/activities index (2026-04-05)
- Clarified policy scope: `activities/` is now a required vanilla comparison reference for **all mod changes with potential structure/path mismatch risk**, not only activity-specific edits.
- Added `/common/activities/00_xianxia_activity_map.txt` as a canonical in-repo index of real in-game files that drive Xianxia activity behavior.
- Added `/common/activities/jianghu_tournament_activity_bridge.txt` as a concise bridge snapshot mapping the Jianghu decision hook to the tournament-hosting event path.
- Workflow requirement: whenever activity-adjacent behavior changes, update both `/common/activities/` index files and `CODEX_CHANGELOG.md` in the same commit.

### 24) Existing-government Xianxia adaptation pass (2026-04-05)
- Implemented broader adaptation of **existing** vanilla governments (feudal, clan, tribal, theocracy, administrative, republic) through `xianxia_apply_government_adaptation_effect`.
- Added dedicated per-government Xianxia modifiers so each vanilla government family receives sect-era fitting bonuses rather than a single generic treatment.
- Added `jianghu_realm_friction` for landed non-cultivator rulers under major temporal governments to reinforce Jianghu-world mismatch pressure.
- Updated `xianxia_world.1000` maintenance event to run adaptation for all landed adult rulers, while retaining high-realm longevity handling for cultivators.
- Added English localization for the new government-adaptation and friction modifiers.

### 25) Sect institutions, staged activities, lineage systems, and fodder sync baseline (2026-04-05)
- Added a fuller sect office layer: new role traits for Inner Hall Elder, Outer Hall Elder, Enforcement Elder, and Lineage Heir, plus periodic assignment flow for landed sect rulers.
- Added sect-internal governance pressure pulses with dispute/power-struggle/resource-obligation outcomes and sect resource stockpile/obligation modifiers tied to realm gameplay.
- Extended Jianghu tournament behavior into a multi-stage chain (`xianxia_world.1100 -> 1110 -> 1120`) with injuries, rivalry generation, and scaled rewards.
- Extended secret-realm expeditions into a progression chain (`xianxia_world.1500 -> 1510 -> 1520`) with staged setbacks and final inheritance outcomes.
- Added a full master-disciple interaction suite: recruit disciple, teach technique, inherit manuals, and expel/betray disciple; added lineage prestige/disciple growth modifiers tied to mentor office traits.
- Reworked alchemy into a two-step pipeline (`xianxia_world.1300 -> 1310 -> 1320`) including furnace-quality scaling (learning gate), failure states, and reward gradients.
- Added a player-facing debug decision/event (`xianxia_debug_state_decision`, `xianxia_world.1900`) that surfaces cultivation stage/sect-role/modifier/cooldown inspection tooltips.
- Performance pass: replaced `every_living_character` loops in cultivation/world orchestration with narrower ruler-scoped iteration and reduced heavy world-adaptation cadence to yearly pulse.
- Added Common-Fodder sync scaffold (`common/fodder/events|gui|localization`) plus `common/fodder/00_runtime_sync_map.txt` and an explicit per-commit mirror update rule.

### 26) Governance deepening, lineage graphing, branching arcs, and sync enforcement (2026-04-05)
- Added council-driven sect politics decisions/events (`convene_sect_council_decision`, `xianxia_world.1720/1730`) with consensus vs deadlock outcomes and downstream struggle pressure.
- Deepened mentor-disciple flow with lineage-oriented flags/variables/opinions and fracture/favor modifier states (`mentor_guidance_opinion`, `lineage_betrayal_opinion`, `sect_lineage_favor`, `sect_lineage_fracture`).
- Upgraded staged chains from single-option flow to branch choices in tournament and expedition mid-stage events (aggressive vs stable tournament bracket; safe vs risky expedition route).
- Added pre-refinement alchemy resource acquisition (`gather_alchemy_resources_decision`, `xianxia_world.1330`) and tied result scaling in refinement outcomes to stocked resource flags.
- Upgraded debug event behavior from static generic tooltips to conditional state readouts keyed to active stage/role/cooldown flags.
- Added automated fodder sync enforcement script (`scripts/check_fodder_sync.py`) and documented the command in the sync map header.

### 27) Review-fix hotpatch: startup initialization scope + sect office scope correctness (2026-04-05)
- Restored startup initialization sweep in `cultivation_character_initialization.0001` from ruler-only to `every_living_character` so unlanded courtiers/children receive immediate meridian/cultivation setup at lobby start.
- Fixed yearly sect office pass faith comparison in `xianxia_world.1700` to compare courtiers against the current iterated ruler scope (`faith = prev.faith`) rather than invalid `root` assumptions under `scope = none`.
- Hardened office reroll exclusivity by explicitly removing all conflicting elder office traits before assigning a new one, preventing trait stacking across yearly rerolls.

### 28) Decision visibility/localization/picture hotfix + sect-founding constraints (2026-04-05)
- Fixed interaction-load blocker in `cultivation_teach_interactions` by replacing invalid AI recipient buckets (`siblings`/`parents`) with valid `family`, restoring disciple interaction registration in game.
- Added missing decision picture references for all `summon_qi` decisions to stop decision-picture missing-entry errors.
- Added UTF-8 BOM where missing in key cultivation files (including `xianxia_world_l_english.yml` and cultivation script files flagged by lexer warnings) to stabilize localization/script loading.
- Updated `found_sect_domain_decision` to enforce county/duchy-tier-only eligibility and set governance to `clan_government` on successful sect founding as a sect-government approximation.

### 29) AI disciple recruitment weight + lineage-heir persistence hotfix (2026-04-05)
- Fixed `recruit_disciple_interaction` AI willingness from zeroed baseline to a non-zero base with meridian-sensitive weighting, so AI courts can actually recruit disciples in play.
- Moved `sect_lineage_heir` out of the mutually-exclusive `education` group into `personality` to preserve inheritance outcomes across yearly sect office reassignment pulses.

### 30) Teach-technique anti-spam cooldown guard (2026-04-05)
- Added explicit validity/cooldown gating to `teach_technique_interaction` so a disciple with `teach_technique_cooldown` cannot be repeatedly farmed for immediate XP/prowess/prestige loops.
- Added a 1-year recipient cooldown flag application on successful teach-technique acceptance.


### 22) Cultivation maintenance + alchemy expansion + UTF-8-BOM policy (2026-04-05)
- Added a repository rule for cultivation content: save edited mod files in UTF-8-BOM encoding to avoid parser/localization loader errors.
- Fixed multiple cultivation script/runtime errors reported in `error.log` (invalid opinion triggers, invalid lifestyle/prowess effects, invalid nickname effect usage, invalid alliance trigger usage, and malformed trait variable increments).
- Fixed disciple recruitment flow so already-awakened courtiers can still be recruited into the sect disciple system, restoring mentor/disciple progression interactions.
- Updated awaken-meridians decision so awakened courtiers/vassals are converted into the awakener's sect faith.
- Restricted elder-role assignment to higher cultivation realms (Core Formation and above); lower-realm cultivators are forced into disciple track.
- Added three-tier alchemy body traits (`alchemy_body_tier_1/2/3`) and tied tier scaling directly into spirit pill success chances.
- Added pill economy decisions to sell refined pills for spirit stones (gold) and buy breakthrough pills (with chance for a lifestyle-speed buff via Enlightenment Pill).
- Added AI pre-breakthrough pill support event that has weaker AI cultivators seek pill support from more learned in-court cultivators.
- Updated sect council / alchemy gathering flows to initiate real activities when hostable (feast/hunt) while preserving existing xianxia event chains.
- Added missing localization coverage for weapon path traits, sect role character descriptions, and new alchemy content.

- Added crafted-pill enlightenment chance: successful spirit pill refinement can now also roll `alchemy_enlightenment_pill` (temporary lifestyle-speed gain).
- Added alchemy body tiers into the initialization special-lottery pools so alchemy physiques can appear naturally like other rare innate gifts.

- Added alchemy lifestyle mastery tiers (XP from repeated pill crafting) with intentionally minor craft-boost behavior compared to innate alchemy-body tiers.
- Added formation mastery system (3 trait tiers + XP progression) and new formation-body tiers; integrated formation bodies into initialization lottery pools.
- Added `raise_formation_barriers_decision` to deploy lore-accurate defensive arrays that improve county fortification and army defensive battlefield advantage.

- Added marriage AI valuation boosts for alchemy/formation body and mastery traits so these new cultivation paths are preferred in sect matchmaking.

### Changelog rules
- **Encoding rule:** Always save newly edited cultivation mod script/localization files in **UTF-8-BOM** encoding.

### 27) Huxian fox-spirit compatch baseline (2026-04-05)
- Added AI pulse `cultivation_ai.2250` to support fox-demon (`huxian`) compatibility behavior.
- All landed adult Huxian rulers are force-synced to top Yin body tier via `yin_bloodline_3` (with lower Yin tiers removed).
- Added low-frequency AI fox-spirit awakening flow gated by personality (deceptive/seductive/ambitious tendencies), cultivation status, and sect alignment.
- Hard-blocked awakening for orthodox sword and order/formations sect identities (Mount Hua, Heavenly Sword Pavilion, Azure Edge, Ten Thousand Swords Valley, Violet Thunder Blade, Eight Trigrams Palace, Celestial Talisman Hall).
- Added doctrine/sect-scaled fox-spirit reaction mapping through new opinion modifiers:
  - orthodox hate (`-100`),
  - order/formation rejection (`-60`),
  - unorthodox caution (`-20`),
  - vagrant swing (small conditional positive),
  - demonic alliance (`+65`),
  - yin/spirit affinity (`+40`).
- Added persistent character modifier `fox_spirit_awakened` and localization keys for fox-spirit state/opinion feedback.

### 28) Huxian fox-spirit child/meridian/dualcultivation expansion (2026-04-05)
- Expanded `cultivation_ai.2250` so Huxian handling includes children (not only adults), enabling youth fox-spirit awakenings when AI personality/sect gates fit.
- Added spiritborn-or-better guarantee for all Huxian meridians (minimum excellent meridians) and post-awakening spiritual temptation package (`spirit_bloodline_3` plus chance for heavenly meridians / extra spirit body traits).
- Added player parent choice event (`cultivation_ai.2261`) on fox-spirit child awakening: accept or disown; disown path attempts to sever parent relation and applies a permanent disowned-child status modifier.
- Added periodic fox-spirit purge pressure event (`cultivation_ai.2260`) so orthodox sword/order-formation lieges can lethally purge exposed fox spirits over time.
- Added fox-spirit-specific dual cultivation AI acceptance tuning so aligned demonic/yin/unorthodox paths are more willing while orthodox/order paths strongly refuse.
- Added beauty enforcement for awakened fox spirits: `beauty_good_3` is now auto-applied (removing lower beauty tiers) to reflect fox-spirit allure fantasy.

### 29) Fox-spirit cannibal predation branch + mortal hunt backlash (2026-04-05)
- Added `embrace_fox_spirit_predation_decision` so awakened fox spirits can opt into `cannibal` as a dedicated taboo progression branch.
- Added `hunt_mortals_fox_spirit_decision` for landed cannibal fox spirits, triggering `xianxia_world.2261` to grant a strong temporary lifestyle-speed buff (`fox_spirit_mortal_hunt_frenzy`).
- Mortal hunt now applies a major opinion penalty (`opinion_fox_spirit_mortal_hunter`) from all non-fox-spirit characters who are not demonic or unorthodox aligned.
- Added supporting xianxia world event text/modifier localization and data definitions for the predation loop.

### 30) Fox-spirit pulse/performance + parent-resolution hotfix (2026-04-06)
- Removed `cultivation_ai.2250` and `cultivation_ai.2260` from per-ruler orchestrator/bootstrapping triggers to avoid multiplicative full-world loops; these events now rely on their global on_action scheduling only.
- Added missing AI-mother auto-resolution branch for fox-spirit child awakening pending state so children without an eligible AI father no longer remain stuck with `fox_spirit_parent_decision_pending`.
- Corrected AI parent-resolution scope targets so disown/accept outcomes now target the actual AI parent (father/mother), not the awakened child scope.
- Added explicit `title`/`desc` bindings to visible player event `cultivation_ai.2261` so parent accept/disown prompts render narrative localization correctly.
- Added player-notification guard flag (`fox_spirit_waiting_player_parent`) so AI parent auto-resolution does not consume pending state after a human parent has already been notified.

### 25) Fox-demon integration + sect-join recovery hotfix (2026-04-06)
- Normalized duplicated UTF-8 BOM headers in key cultivation script files (`cultivation_ai_events`, `cultivation_effects`, marriage scripted modifiers mirror) to prevent parser misreads that could cascade into missing cultivation effects/events.
- Restored broad AI sect-join coverage by making startup/monthly cultivation orchestration iterate `every_living_character` (AI adults with active meridians), not only rulers.
- Fixed fox-spirit compatibility trigger to key off the actual fox trait (`huxian_blood`), replacing invalid `has_trait = huxian` usage.
- Added a fox-demon possession pulse in `cultivation_ai.2250` so awakened fox demons can occasionally seize random AI children as vessels, immediately binding them into the existing meridian/cultivator/perk pipeline (no separate fox-only progression track).
- Removed the malformed compatch culture definition `fox demon spirits compatch/common/culture/cultures/00_huxian.txt` that was generating parser errors and blocking related fox-demon content from loading reliably.
- Follow-up sect-join reliability tweak (same date): `cultivation_ai.0002` no longer requires pre-existing cultivator trait; it now bootstraps Qi Gathering + first meridian perk for eligible meridianed AI before sect assignment, and checks `has_cultivation_sect_faith` directly to force vanilla-faith ruler conversion into sect faiths.
- Follow-up interaction/fox reliability fix (2026-04-06): `dual_cultivation_interaction` now requires both participants to be adult cultivator lovers/soulmates, includes proper interaction-name localization key, and no longer references Carnalitas scope plumbing. Fox possession now targets only children (age 6-13), guarantees missing-meridian recovery to excellent+, and immediately applies top beauty tier on possession.
- Removed legacy `common/character_interactions/carn_sex_interaction.txt` from core mod load to eliminate unresolved Carnalitas trigger/effect parser errors in `error.log` when external dependency scripts are absent.
- Error-log cleanup follow-up (2026-04-06): added missing BOM to `cultivation_sect_nicknames_l_english.yml` and `20_cultivation_sect_nicknames.txt`, and removed duplicate `cultivation_breakthrough.1400.wait` localization definition.
- Dual-cultivation scope regression fix (2026-04-06): restored `scope:recipient -> carn_sex_partner_scope` save before `dual_cultivation_effect`, and re-enabled scripted-effect fallback scope initialization to avoid undefined-partner runtime failures.

### 24) Fox possession sect-join dead-branch fix + sect confederation range tuning (2026-04-06)
- Fixed an unreachable branch in fox-vessel possession follow-up: possessed targets are children (age 6–13), so sect conversion bootstrap now no longer hard-requires `is_adult = yes`.
- Possessed hosts now always receive `cultivation_qi_gathering` if missing before sect assignment checks, ensuring the possession flow can route into sect faith conversion logic.
- Tuned same-sect defensive-pact formation so rulers form cross-realm confederation-style alliances when either:
  - they are within diplomatic range, or
  - both rulers are above Qi Gathering (Qi Refining+), effectively granting long-range sect coalition behavior to higher realms.

### 31) Fox-spirit disown parser hotfix (2026-04-06)
- Removed unsupported `remove_relation` effects from fox-spirit parent disown branches in `cultivation_ai.2250` / `cultivation_ai.2261`.
- Disown outcomes now apply the permanent `fox_spirit_disowned_child` modifier and clear pending/waiting flags without invoking invalid effects, preventing parser cascade errors that hid downstream fox-spirit events.

### 32) Singular reincarnation lottery ruler system (2026-04-06)
- Added monthly global event `cultivation_ai.2270` that creates exactly one active "reincarnation monster" among landed count+ rulers when no active holder/cooldown exists.
- Selected ruler is forced to `cultivation_true_immortal`, upgraded to `heavenly_meridians`, and granted the full cultivation perk chain to simulate a maxed-out xianxia reincarnator.
- Added singleton control flags:
  - `cultivation_reincarnation_active` while a living holder exists,
  - `cultivation_reincarnation_holder` on the chosen ruler,
  - `cultivation_reincarnation_cooldown_anchor` (200 years on a random living anchor character) applied only after holder death before next roll.
- Reincarnation lottery winners now receive dedicated nickname `the Reincarnator` (`nick_the_reincarnator`) on assignment for immediate world readability.
- Hooked `cultivation_ai.2270` into `on_monthly_pulse` for continuous world-state maintenance.

### 33) Reincarnation lottery eligibility/teardown correctness fix (2026-04-06)
- Replaced invalid reincarnation candidate tier filter with explicit `highest_held_title_tier` checks (count/duchy/kingdom/empire) so landed count+ rulers are selected correctly.
- Tightened active-holder teardown to require a *living, landed, count+* holder; if holder is dead/unlanded/ineligible, singleton state now clears and cooldown begins.
- Added candidate scope save + existence guard before applying reincarnation package/global-active flag to prevent active-state flips when no valid candidate exists.

### 34) High-realm portrait transformation pass + fox-spirit white hair (2026-04-06)
- Added `activities/trait_portrait_modifiers/zz_xianxia_trait_modifiers.txt` to introduce visible, lore-style physical progression for high cultivation realms.
- High realm portrait shaping now ramps from Heavenly Being through True Immortal with gradual height increase and progressively more refined/slender immortal body silhouettes.
- Added hair-color whitening at Entering Nirvana and full silver-white hair at True Immortal to reinforce ascension fantasy.
- Added universal white-hair portrait override for `huxian_blood` so fox demons consistently present the requested fox-spirit appearance.
- Follow-up fix: inserted missing `cultivation_four_axis` portrait stage between Heavenly Being and Integration to prevent mid-realm visual regression during breakthrough progression.
- Added escalating golden-eye portrait tint (`eye_color`) for high-realm cultivators from Heavenly Being through True Immortal.
- Added faith-aspected eye overrides for cultivators: demonic-faith cultivators now tint red eyes, and unorthodox-faith cultivators tint purple eyes.
- Scoped all white-hair portrait overrides (Nirvana/True Immortal + `huxian_blood`) to demonic or unorthodox faith cultivators only.
- Added a demonic-path blood-red hair variant (wrathful/sadistic/vengeful archetypes) for Entering Nirvana/True Immortal and `huxian_blood`, while preserving white hair for unorthodox and non-bloodthirsty demonic cultivators.

### 35) Cultivator body archetype pass from personality/education/lifestyle (2026-04-06)
- Added a new portrait modifier group `xianxia_cultivator_body_archetypes` to map body-shape DNA toward lore-style xianxia ideals based on character identity traits.
- Added `xianxia_disciplined_immortal_frame` for temperate/diligent/athletic and high learning/stewardship cultivators, nudging bodies toward a leaner disciplined silhouette.
- Added `xianxia_martial_hero_frame` for martial-focused personalities/education/traits (brave, wrathful, blademaster, hunter, high martial education), with a taller and stronger heroic frame.
- Added `xianxia_refined_sage_frame` for calm/patient/humble/scholar-theologian-mystic leaning cultivators, emphasizing an elegant refined immortal body line.
- Added `xianxia_indulgent_deviation_frame` so indulgent paths (gluttonous/lazy/drunkard/hashishiyah/reveler) visibly diverge from orthodox cultivation physiques unless counterbalanced by elite body-discipline traits.
- Follow-up regression fix (same date): moved Nirvana/True Immortal demonic/unorthodox white-hair gating into dedicated hair-aspect modifiers so high-realm eye/body/height transformation progression now applies to all faith paths again.


### 37) Heavenly Demon proclamation + path-based sect opinion cleanup (2026-04-09)
- Added a new major decision `declare_heavenly_demon_decision` for rulers of `blood_moon_demonic_sect` (Heavenly Demon Sect) who reach empire-scale conquest (`realm_size >= 80`) to proclaim themselves the Heavenly Demon.
- Proclamation now grants permanent modifier `heavenly_demon_proclaimed` with very high same-faith opinion boost and strong learning/lifestyle growth bonuses, plus `nick_the_heavenly_demon`.
- Updated cultivation path tenets so `different_faith_opinion` penalties from path tenets are no longer applied at sect level (`0`), preventing same-path/different-sect cultivators from receiving automatic hostility just for sect mismatch.
- Added yearly path-opinion normalization pulse `cultivation_ai.2280` with explicit path-based relationship outcomes: same-path cultivators receive `opinion_cultivation_path_peer`, while different-path cultivators receive `opinion_cultivation_path_rival` (`-40`).

- Decision availability now checks for any living existing Heavenly Demon holder (`heavenly_demon_proclaimed`); once no living Heavenly Demon remains, a new qualified ruler can proclaim again.


### 38) Great sect titles + martial confederation groundwork (2026-04-09)
- Added new orthodox sect faith seeds for future Jianghu expansion: `beggar_sect`, `tang_clan`, and `emei_sword_sect` under `cultivation_orthodox`.
- Added two new major decisions:
  - `proclaim_great_sect_hegemon_decision` (great-sect title framework for independent sect rulers),
  - `found_martial_confederation_decision` (path-level confederation foundation).
- Added new persistent modifiers `sect_hegemon_mandate` and `martial_confederation_founder` with prestige/opinion/lifestyle support.
- Added scripted effect `cultivation_form_path_confederation_pacts_effect` and new maintenance event `cultivation_ai.3002` to form/repair cross-sect same-path alliances over time.
- Hooked `cultivation_ai.3002` into monthly pulse as a low-cost confederation baseline for future path-level alliance systems.


### 39) Orthodox/Demonic alliance leadership and imperial-sect gate (2026-04-09)
- Added additional classic Jianghu sect faith seeds (Qingcheng, Kunlun, Kongtong, Diancang) plus `heavenly_mandate_bureau` as an imperial-backed orthodox lane.
- Added demonic alliance faith seeds (`yin_yang_harmony_sect`) to mirror common xianxia/manhua faction structures.
- Added alliance leadership decisions: `proclaim_orthodox_alliance_leader_decision`, `proclaim_demonic_alliance_leader_decision`, and `convene_martial_alliance_decision`.
- Added `establish_heavenly_mandate_bureau_decision`, gated to rulers with `primary_title = e_china` or `culture = han`, to tie imperial sect identity to requested imperial/Han constraints.
- Added supporting alliance/imperial modifiers and localization so this set functions as a foundation for deeper confederation and Jianghu institution systems.


### 40) Heavenly Mandate Bureau Han-majority startup alignment (2026-04-09)
- Added startup event `cultivation_ai.2290` to align the `e_china` holder to `heavenly_mandate_bureau` on game start when eligible.
- Added Han-majority seeding on game start: Han-culture orthodox sect rulers now convert to `heavenly_mandate_bureau` at a 70% pass, establishing a clear majority baseline for the Imperial/Heavenly Mandate lane.


### 41) Hidden sect/path identity backend for shared cultivation trees (2026-04-09)
- Added hidden sect signature modifiers (`sect_signature_orthodox_hidden`, `sect_signature_demonic_hidden`, `sect_signature_unorthodox_hidden`, `sect_signature_vagrant_hidden`, `sect_signature_imperial_guard_hidden`) and hidden path identity modifiers (`path_internal_cultivation_hidden`, `path_external_cultivation_hidden`, `path_balanced_cultivation_hidden`, `path_tyrannical_cultivation_hidden`, `path_longevity_cultivation_hidden`).
- Added CK3-safe scripted-effect glue to refresh sect signatures by faith and to assign mutually-exclusive path identities through perk effects (`cultivation_set_path_*_effect`).
- Added monthly identity refresh event `cultivation_ai.2295` (hooked to monthly pulse) so sect/path backend identity stays synchronized for AI and player states.
- Updated representative perks in Mortal, Qi Gathering, Qi Refining, Four Axis, and Integration trees to grant hidden path identities and add AI branch-selection bias aligned to sect signatures.
- Added anti-conflict guard with random sect lottery assignment (`cultivation_random_sect_lottery_assigned`) so game-start Han mandate seeding does not override rulers already assigned by sect lottery effects.

- Path-opinion yearly pass performance fix: `cultivation_ai.2280` now scopes to independent rulers in diplomatic range (avoids global O(n²) ruler pairing), and clears stale `opinion_cultivation_path_peer`/`opinion_cultivation_path_rival` before applying the current path relationship.

### 42) Jianghu insult + ambush interaction import pass (2026-04-10)
- Added two new xianxia-native hostile interactions inspired by external reference mods (Insult to Injuries / Cultivator Indulgences style social aggression):
  - `jianghu_face_slap_interaction` for public humiliation / face-slapping social conflict.
  - `jianghu_set_ambush_interaction` for covert retaliation against weaker targets.
- Both interactions are explicitly realm-gated for xianxia balance:
  - Actor must be a cultivator.
  - Ambush actor must be at least respected realm tier (Nascent Soul+ via existing triggers).
  - Targets are constrained to mortals or lower-tier cultivators (Qi Gathering -> Core Formation), preventing top-realm grief loops.
- Added jianghu-specific opinion modifiers and English localization for interaction descriptions.
- Design intent: strengthen interpersonal grudges/retaliation fantasy in jianghu without breaking established high-realm invulnerability direction.

### 43) Cross-mod social integration pass: IR + RV + SRE inspirations (2026-04-10)
- Expanded jianghu interaction layer with additional Rescue & Vengeance-inspired social tools:
  - `jianghu_demand_prisoner_release_interaction` for coercive captive rescue diplomacy.
  - `jianghu_swear_blood_vengeance_interaction` for formalized revenge feuds after memory-backed bereavement.
- Added corresponding opinion fallout for forced rescues and blood-feud declarations.
- Added hidden monthly social pulse events (`xianxia_social.1000`, `xianxia_social.1100`) inspired by Inheritable Relations + Social Relations Expanded:
  - Heirs inherit partial friendship/rivalry opinion fallout from predecessor social networks.
  - Friend-heavy courts gain social momentum while rival-heavy courts accrue internal dispute pressure.
- Hooked these social events into monthly on_action orchestration to keep jianghu relationship dynamics persistent over campaign time.

### 44) Long-lived cultivator social memory duration rebalance (2026-04-10)
- Extended jianghu social opinion durations (humiliation, ambush, rescue coercion, blood vengeance, inherited friendship/rivalry) from short mortal-scale timers to long cultivation-scale windows.
- Increased interaction-applied opinion durations to multi-decade/century-scale values so major slights and blood-oaths persist across long-lived cultivator lifespans.
- Increased inheritable social fallout event durations so predecessor alliances/feuds remain politically relevant through long cultivation reigns.

### 45) Jianghu rescue-opinion target fix + localization BOM compliance (2026-04-10)
- Fixed `jianghu_demand_prisoner_release_interaction` so `opinion_jianghu_forced_rescue` is applied by the jailer (`scope:recipient`) toward the rescuer (`scope:actor`) after release, rather than accidentally by the released prisoner scope.
- Re-encoded `xianxia_jianghu_interactions_l_english.yml` with UTF-8 BOM to match CK3 localization loading expectations and in-repo localization conventions.

### 46) Face-slap system polish from Insult to Injuries pattern + localization recovery (2026-04-10)
- Reworked `jianghu_face_slap_interaction` to include a direct lifestyle progression debuff modifier (`jianghu_face_loss`) so public humiliation impacts long-term cultivation growth, not only opinion/stress.
- Added dedicated letter event `xianxia_jianghu_letters.1000` using an Insult to Injuries-style letter-event structure (sender/opening/branching desc/options) for player-facing humiliation messaging.
- Cleaned and rebuilt `xianxia_jianghu_interactions.txt` to remove accidental stray scope effects from prior merge/edit churn.
- Rebuilt English localization with UTF-8 BOM and added missing opinion localization keys (including compatibility alias for typoed key `opinion_jianghu_public_humilation`) to prevent raw-key display in UI.

### 25) Magic Treasure crafting framework + xuanhuan artifact pool (2026-04-10)
- Added a new major decision, `craft_magic_treasure_decision`, available to cultivators with the new `magic_treasure_crafter` trait track.
- Implemented a 3-tier crafter trait progression (`magic_treasure_crafter_1/2/3`) where higher tiers improve artifact quality/wealth rolls and reduce cooldown burden per craft.
- Added `xianxia_world.1800` forge event that presents a clear craftable artifact roster and ties decision flow into event-driven artifact generation.
- Added `xianxia_magic_treasure_craft_effect` plus ten xianxia/xuanhuan-themed artifact creation effects (blade, gourd, cauldron, robe, banner, etc.) using CK3 artifact creation scripting patterns.
- Added dedicated artifact template + new artifact modifiers file for generated relic bonuses, along with full English localization for decision/event/traits/artifact names and descriptions.

### 47) Legendary world-artifact death-run decision chain (2026-04-10)
- Added `seek_legendary_world_artifact_decision` for high-realm cultivators seeking forbidden world relics.
- Decision starts event `xianxia_world.1810` with an explicit ultra-lethal design: if the player forces entry without extreme stats, outcome is near-certain death (92% fatal).
- Added high-stat pass gate option requiring extreme personal attributes (Learning/Prowess 45+ or Intrigue/Stewardship 35+), allowing a survivable branch with large rewards.
- Added two new state modifiers: `legendary_artifact_finder` (major success boon) and `legendary_artifact_escape_wounds` (severe failed-attempt penalty).

- Expanded magic treasure pool with 30 additional craftable artifacts (total pool now 40) and wired all new artifact creation effects/modifiers/localization into the existing craft decision flow.
- Expanded pill creation system with multi-formula grand refinement via `refine_grand_spirit_pills_decision` and event `xianxia_world.1830` (Body Tempering, Soul Clarity, Tribulation Guard, Blood Ignition).
- Added `host_jianghu_artifact_auction_decision` and event `xianxia_world.1820` to run tiered artifact bidding (mortal/profound/heaven) or sell your own treasures for gold/prestige.
- Added a rare Legendary Breakthrough Pill discovery hook to the legendary artifact/auction chains; when found, it guarantees the holder's next breakthrough attempt (100% success) and is consumed on use.
- Added `study_magic_treasure_crafting_decision` + `xianxia_world.1840` so Magic Treasure Crafter tiers can be earned in normal gameplay instead of requiring external trait injection.
- Updated auction sell branch to actually destroy one owned artifact before granting sale payout, restoring real tradeoff economics.
- Added `invite_path_cultivators_decision` + `xianxia_world.1850` to recruit path-aligned wandering cultivators into court champions, with character generation fallback only when no suitable wanderers exist.
- Added spirit-stone economy pressure to breakthrough decisions: attempts now require minimum gold and apply longer resource cooldowns at low reserves, slowing both player and AI progression when poor.
- Added non-cultivator stat cap enforcement effect (`xianxia_non_cultivator_stat_cap_effect`) that clamps diplomacy/martial/stewardship/intrigue/learning/prowess to 9 for non-cultivators during world maintenance pulses.
- Added a disciple-assignment activity-style chain (`disciple_assignment_activity_decision` -> `xianxia_world.1860`) that assigns talented non-adult disciples to cultivator mentors, generating a mentor only when none exist.
- Revamped jianghu gathering into a staged activity-style event chain (`jianghu_grand_gathering_activity_decision` -> `xianxia_world.1870/1871/1872`) with tournament-like phased outcomes and hosting momentum rewards.
- Added `host_same_path_dao_exchange_activity_decision` with staged events (`xianxia_world.1880/1881`) as a feast-like same-path sect meeting that concludes with lifestyle speed buffs from Dao exchange for host and participants.
