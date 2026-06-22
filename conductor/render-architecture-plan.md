# Faith Points - Video Rendering Architecture Plan

## Background & Motivation
The "Faith Points" channel requires a highly retentive, visually striking video format described as "Realismo Sagrado Noir" combined with the "Protocolo do Fragmento". To achieve this efficiently and at scale, we are building a headless video rendering pipeline designed specifically for execution in Google Colab. The pipeline will transition from static images to dynamic text revelations and impactful keyword overlays, synchronized with cinematic audio.

## Scope & Impact
*   **Target Environment:** Google Colab (Headless Linux environment).
*   **Core Engine:** `MovieLite` (selected for high performance, Numba JIT compilation, and MoviePy-like developer experience).
*   **Output:** High-quality `H.264` `.mp4` video files optimized for YouTube/Shorts retention.
*   **Visual Logic:** Implementation of slow continuous zooms, custom torn-paper masks, and synchronized typography.

## Proposed Solution
We will build a modular Python application leveraging `MovieLite` as the primary sequencer and orchestrator.

### 1. Technology Stack
*   **Compositor:** `MovieLite` (fast rendering, timeline management).
*   **Image Processing:** `Pillow` (`PIL`) + `numpy` (for complex matrix manipulations like the continuous slow zoom and dynamic masking if MovieLite's built-in tools need supplementing).
*   **Audio Processing:** `MovieLite`'s audio module (for mixing voiceover with synthetic drone backgrounds).

### 2. Architectural Modules
The system will be divided into distinct functional classes:

*   **`NoirEnvironment`:** Handles the background layer.
    *   Accepts a base image (e.g., the iron anvil with coins).
    *   Applies a continuous, mathematically calculated slow-zoom (Scale and Position Motion).
    *   Applies a color grading overlay (deep shadows, amber highlight).

*   **`FragmentMask`:** Manages the "Protocolo do Fragmento".
    *   Loads an alpha-channel PNG of a distressed/torn edge.
    *   Orchestrates the transition: Fade in the mask over the background.
    *   Manages the "Typewriter Effect": Programmatically revealing the Bible verse text within the bounds of the mask.

*   **`MacroConceptDisplay`:** Handles the keyword impacts.
    *   Triggers the displacement/shrinking of the `FragmentMask`.
    *   Overlays the golden, serif keyword (e.g., "THE COST OF LOYALTY") directly onto the dark background.

*   **`AudioOrchestrator`:**
    *   Generates or loads the low-frequency C2 synthetic drone.
    *   Mixes the drone with the primary voiceover track.

## Implementation Steps

1.  **Environment Setup:** Create a `requirements.txt` specifically for the Colab environment (including `movielite`, `pillow`, `numpy`).
2.  **Asset Preparation:** Define the structure for inputs (background image, voiceover audio, text JSON/YAML file).
3.  **Module Development:**
    *   Implement the slow-zoom logic.
    *   Implement the typewriter text effect layer.
    *   Implement the macro concept overlay layer.
4.  **Pipeline Assembly:** Write the `main.py` orchestrator that takes the inputs and sequences the modules sequentially in the MovieLite timeline.
5.  **Colab Wrapper:** Create a simple entry point or Jupyter Notebook cell structure to trigger the render.

## Verification & Testing
*   **Render Test:** Execute a test render of the first 15 seconds (The Hook phase) using dummy assets.
*   **Performance Benchmark:** Ensure the render time in a Colab environment is substantially faster than real-time (e.g., a 15-second clip should render in < 5 seconds).
*   **Visual Audit:** Verify the "câmera viva" (zoom) does not stutter, the mask edges are clean, and the text timing aligns with the aesthetic intent.