# React Design to TYPO3 Migration

Skills that turn a React mockup (Lovable, Stitch) into an editable TYPO3 site built on Astryx, via evidence-backed handoffs between extraction, analysis and build.

## Language

**Migration bundle**:
The versioned set of handoff artifacts for one design, stored in the consumer project.
_Avoid_: session state, workspace

**Handoff**:
A versioned JSON artifact with a readable Markdown report that one skill produces and another consumes. Carries source provenance, dependencies and a revision.
_Avoid_: output file, export

**Binding requirements**:
Target-neutral facts in a component spec: content parts, cardinality, defaults, assets and behavior. Changing them makes dependents stale.
_Avoid_: requirements (unqualified)

**Target hypothesis**:
The analyze skill's non-binding proposal for placement and fields. Build adopts or overrides it with a recorded reason; an override does not make the spec stale.
_Avoid_: placement decision, mapping

**Placement class**:
The kind of TYPO3 home a component is hypothesized to have: content element, nested container, reusable native component, or page-layout part.
_Avoid_: type, target type

**Placeable element**:
A content element or Content Block that an editor can put into a container column.
_Avoid_: widget, block (unqualified)

**Embedded component**:
A native Fluid component used inside a template; it cannot be placed in a container column.
_Avoid_: partial

**Composite section**:
A mockup section made of a layout plus child components. Whether it is one spec or a parent spec referencing child specs is decided by the user per case.
_Avoid_: group

**Reuse disposition**:
Build's chosen outcome for a component: configure, compose, extend, or create new.
_Avoid_: strategy


**Decision gate**:
A point where a skill stops and asks the user to choose (analysis scope, Fluid Styled Content conflict, recipe gap, fidelity deviation). The answer is recorded in the handoff's `decisions` and reused by later sessions; unanswered, it blocks or marks the artifact incomplete.
_Avoid_: confirmation prompt, approval step
