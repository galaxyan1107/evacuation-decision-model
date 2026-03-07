# Naval Force Posture

The U.S. has assembled its largest Middle East military buildup since the 2003 Iraq invasion. Naval force posture is a key stabilizing input to the HAM feedback gain model.

## Carrier Strike Groups Deployed

### CSG-3: USS Abraham Lincoln (CVN-72)
- **Location:** Arabian Sea (since late January 2026)
- **Redirected from:** South China Sea / Indo-Pacific
- **Air Wing:** Carrier Air Wing 9 (CVW-9)
  - F/A-18E/F Super Hornets
  - EA-18G Growlers (electronic warfare)
  - E-2D Advanced Hawkeyes (AEW&C)
  - MH-60R/S Seahawks
- **Escorts:** USS Spruance (DDG-111), USS Michael Murphy (DDG-112), USS Frank E. Petersen Jr. (DDG-121)
- **Operation:** Epic Fury

### CSG-12: USS Gerald R. Ford (CVN-78)
- **Location:** Eastern Mediterranean Sea
- **Deployed:** En route from mid-February 2026
- **Significance:** Uncommon two-carrier deployment — signals high readiness
- **Operation:** Epic Fury

## Independent Destroyers in Arabian Sea

| Ship | Hull | Role |
|------|------|------|
| USS McFaul | DDG-74 | BMD / Strike |
| USS John Finn | DDG-113 | BMD / Strike |
| USS Milius | DDG-69 | BMD / Strike |
| USS Delbert D. Black | DDG-119 | BMD / Strike |
| USS Pickney | DDG-91 | BMD / Strike |
| USS Mitscher | DDG-57 | BMD / Strike |

**Total: 6 independent guided-missile destroyers** with Aegis BMD capability, plus 3 CSG escorts = 9+ Aegis-capable ships in theater.

## Additional Assets

- Warships positioned in the Strait of Hormuz
- Littoral Combat Ships in the Persian Gulf
- Red Sea naval presence
- Submarine assets (classified positions)

![Naval Force Posture — Operation Epic Fury](../assets/naval_posture.png)

## Model Integration

Naval force posture feeds into the HAM stability model through two channels:

### 1. Interception Rate Support
The Aegis BMD-capable destroyers supplement THAAD and Patriot land-based systems. The 9+ Aegis ships provide layered defense that supports the >92% interception rate. This is modeled as a **stabilizing factor** in the λ calculation.

### 2. Escalation Deterrence
The two-carrier deployment creates a credible deterrent against further escalation. This affects:
- **Proxy activation probability:** Reduced from 8% to 6% (Houthi/Hezbollah less likely to join with 2 CVNs in theater)
- **Hormuz closure risk:** Reduced from 6% to 4% (naval dominance deters blockade attempts)
- **Regime War scenario prior:** The massive force posture makes full-scale regime war less likely (reduced from 0.20 to 0.15 prior)

### Lambda Impact

```
λ_naval_deterrence = -0.08 · carrier_count · (1 + N(0, 0.10))
```

With 2 carriers: approximately -0.16 additional stabilizing effect, further pulling λ below the cascade threshold of 1.0.
