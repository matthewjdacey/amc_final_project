### Final Project – Algorithmic Music Composition (CS150)

## Group members
Matthew Dacey (mdacey02), Sam Lev (slev01), Begüm Ugurlu (bugurl01), Kimaya Vaid (kvaid01)

Submitted by Sam Lev (slev01)

## Introduction
This project implements a multi-algorithm, fugue-inspired composition system that generates a complete three-voiced musical work plus harmonic accompaniment. Rather than using a single algorithm in isolation, this project integrates several algorithmic approaches—Monte Carlo methods, Serialism, Genetic Algorithms, and Grammar-Based Structure—to produce a cohesive, musically meaningful piece inspired by the architecture of a Bach fugue.

The goals of this project were:
1. **Blend multiple algorithms into a coherent musical system**, rather than using each technique in isolation.  
2. **Recreate the structural feel of a Bach fugue** using algorithmic methods.  
3. **Engineer interactions between algorithms** so the musical lines reinforce each other instead of clashing.  
4. **Produce output that is musically intelligible**, not merely technically correct.

## Command-Line Arguments
The program can be run manually from the directory containing all project files with `python3 project.py`

The 0 or more of the following command-line flags can be added:
- `-s` will create a file called `out.xml` with sheet music of the generated piece
- `-m` will create a file called `out.midi` of the generated piece
- `-fixed` will fix the random number generators to determinisitically generate the same piece as was presented in class

Executing the `run_project.sh` script will run the program with all 3 arguments, deterministically generating both an xml and midi file.

## Files
- `answer.py` generates an answer to the subject using serialism
- `chords.py` generates chord progression for the full piece
- `counter_subject.py` generates a harmonious counter subject using a genetic algorithm
- `grammar.py` derives the high-level structure of the composition from our encoded grammar
- `project.py` contains the main program control flow; manages all of the voices and roles; and renders the piece to music21
- `rhythm_gen.py` generates related and interacting rhythms for the subject and counter-subject
- `subject.py` generates a pitch sequence for the subjects of the piece
-  `top_level.py` contains top-level global constants and functions


## High-Level Overview
Each algorithm is paired with a specific musical role from traditional fugue writing:
  
- **Subject** – the main melody of the fugue. Must be memorable, consistent, and rhythmically recognizable.
   - Implemented using **Monte Carlo** (controlled randomness that maintains stylistic constraints).
- **Answer** – an imitation of the subject, typically transformed. Needs to imitate and resemble the subject.
   - Implemented using **Serialism-style transformations** (rotation, doubling, rhythmic shifts).
- **Counter-Subject** – an independent melody accompanying the subject. Must remain consonant, balanced, and musically supportive.
   - Implemented using **two Genetic Algorithms**:
       - One for **pitch** (interval-based fitness vs the subject)  
       - One for **rhythm** (a “thermodynamic” model balancing rhythmic density across voices)

The composition is organized into **three melodic voices** plus a **fourth harmonic voice**:
- **Voice 1:** Subject / Answer / Counter-Subject (octave-up register)
- **Voice 2:** Subject / Answer / Counter-Subject
- **Voice 3:** Subject / Answer / Counter-Subject (octave-down register)
- **Voice 4:** Automatically generated chordal harmony (whole-note chords)

Total length: **96 bars**, divided into  
- 32-bar Exposition  
- 32-bar Development  
- 32-bar Final Section  

Each 8-bar phrase receives an algorithmically determined role for each voice.

## System Architecture

### 1. Grammar-Based Structure (Global Form)

The global structure of the piece is defined by a **probabilistic grammar**, which assigns these roles across an Exposition, Development, and Final Section. A weighted grammar generates a 96-bar piece organized as:
- **32-bar Exposition**
- **32-bar Development**
- **32-bar Final Section**

Each 8-bar phrase receives an algorithmically determined role for each voice:
- `S` – Subject  
- `A` – Answer  
- `C` – Counter-Subject  
- `_` – REST  

Patterns like `"SC_"`, `"AC_"`, or `"CCC"` are drawn via weighted probabilities and then randomly permuted among the three melodic voices, ensuring variety while preserving structure.

---

### 2. Subject – Monte Carlo Rhythm + Constrained Pitch Walk
The subject must be recognizable and balanced, so we built it with:

- **Monte Carlo rhythm generator**  
  - Adaptive probabilities encourage downbeat alignment, cadential long notes, and stepwise rhythmic clusters.
- **Pitch generator with tonal constraints**  
  - Stepwise motion, limited leaps, no repeats, and stable opening/ending.

This gives the subject a cohesive identity.

---

### 3. Answer – Serialism Transformations
The Answer should resemble the subject but be clearly transformed.

**Novel Approach**: Instead of using 12-tone rows, we treat the subject itself as a “row” and apply serial transformations These transformations become progressively more varied, creating functional fugue-like answers rather than atonal ones.

We apply one of four serial operations:
- Rotate pitch row  
- Rotate rhythm sequence  
- Double notes  
- Double the entire sequence at half-duration  

This yields immediate recognizability without duplication.

---

### 4. Counter-Subject – Dual Genetic Algorithms
The counter-subject must work *with* the subject, not compete with it.  
We design that through two GAs:

**Pitch GA**  
- Chromosomes = pitch sequences  
- Fitness = interval consonance against the subject  
- Selection uses a **normal distribution** centered on a target similarity coefficient  
- Produces lines dominated by 3rds, 6ths, and octaves

**Rhythm GA**  
- Chromosomes = rhythmic sequences  
- Fitness based on “thermodynamic balance”:  
  - If the subject is rhythmically dense, counter-subject becomes simpler  
  - If subject is sparse, counter-subject increases activity  

This creates real contrapuntal interaction.

---

### 5. Harmonic Voice – Rule-Based Chords
A fourth voice provides functional harmonic grounding using simple triads with constraints:
- Section endings must cadence on C major  
- Leading-tone chord resolves correctly  
- Unstable chords require specific successors  

This keeps the texture tonal.

---

## Technologies & Skills Demonstrated
- Python, music21
- Monte Carlo simulation
- Genetic Algorithms (multi-objective fitness)
- Serial transformations
- Grammar-based generative models
- Music theory: fugue structure, counterpoint, harmony
- Algorithmic integration & system design

---

## Authors
Kimaya Vaid, Matt, Sam




