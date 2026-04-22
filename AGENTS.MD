# AGENTS.MD

This file defines practical coding standards for building and maintaining this Pygame project.

## 1. Core Principles

- Keep gameplay code simple, readable, and deterministic.
- Prefer small, focused functions over long multi-purpose blocks.
- Separate update logic from render logic.
- Optimize only after identifying real bottlenecks.

## 2. Project Structure

- `main.py`: entrypoint, main loop, scene/state bootstrap.
- `assets/sprites/`: sprite classes and UI/gameplay visual components.
- `assets/sounds/`: sound loading and playback utilities.

Rules:

- Avoid circular imports.
- Keep asset paths centralized in constants or a dedicated config section.
- Group related behavior in classes (player, enemy, HUD widgets, screens).

## 3. Python Style Conventions

- Follow PEP 8 naming:
	- `snake_case` for functions and variables.
	- `PascalCase` for classes.
	- `UPPER_SNAKE_CASE` for constants.
- Add type hints for public methods and non-trivial functions.
- Use docstrings for classes/functions with non-obvious behavior.
- Keep functions short (target ~20-40 lines where reasonable).

## 4. Pygame Game Loop Standards

- Use a single `clock = pygame.time.Clock()`.
- Frame cap with `clock.tick(FPS)`.
- Use delta time for movement and time-based effects:
	- `dt = clock.tick(FPS) / 1000.0`
	- position updates should use `speed * dt`.
- Process events once per frame.
- Maintain loop order:
	1. Handle events
	2. Update game state
	3. Draw frame
	4. `pygame.display.flip()` or `pygame.display.update()`

## 5. Sprite and Entity Design

- All moving/drawable entities should expose clear methods:
	- `update(dt, ...)`
	- `draw(surface)` (if not using group draw directly)
- Prefer `pygame.sprite.Sprite` and `pygame.sprite.Group` for consistency.
- Keep collision rectangles (`rect`) in sync with visual position.
- Use `Vector2` for movement math when direction/acceleration are involved.

## 6. Assets and Resource Loading

- Load assets once, then reuse references.
- Avoid loading images/sounds inside per-frame code.
- Normalize images on load:
	- `convert()` for opaque images.
	- `convert_alpha()` for transparency.
- Handle missing files with clear errors (fail fast during startup).

## 7. Input Handling

- Use event-driven logic for one-shot actions (jump, menu confirm).
- Use key-state polling for sustained actions (movement).
- Avoid mixing duplicate input paths unless intentionally needed.

## 8. Collision and Physics

- Keep collision logic in dedicated functions/methods.
- Resolve movement per axis when needed to reduce tunneling artifacts.
- Prefer explicit constants for physics values:
	- `GRAVITY`, `JUMP_VELOCITY`, `MAX_SPEED`, `ACCELERATION`.

## 9. UI and Screens

- Keep menu/death/pause screens as separate components or states.
- Do not mix gameplay update logic into UI screen classes.
- Render text/fonts through small helper utilities to avoid repetition.

## 10. Audio Practices

- Separate SFX and music volume controls.
- Prevent repeated sound spam for events triggered every frame.
- Preload commonly used SFX and reuse channels when practical.

## 11. Error Handling and Logging

- Validate critical startup dependencies (assets, fonts, mixer init).
- Raise descriptive exceptions for unrecoverable resource errors.
- Use lightweight debug logs/prints behind a `DEBUG` flag.

## 12. Performance Checklist

- Keep per-frame allocations low.
- Avoid expensive operations in `update()` when they can be cached.
- Limit full-screen alpha blending and repeated surface scaling.
- Profile first if FPS drops (`cProfile`, frame timing prints).

## 13. Testing and Verification

Minimum checks before commit:

- Game launches with no traceback.
- Player/input still works as expected.
- Death/win/game-over flows still trigger correctly.
- No new missing-asset errors.
- No obvious FPS regression.

## 14. Git and Change Hygiene

- Keep commits focused and small.
- Do not refactor unrelated systems in feature/fix branches.
- Update this file when introducing new architectural patterns.

## 15. Suggested Development Flow

1. Reproduce or define the gameplay/task change.
2. Implement the smallest correct code change.
3. Run and verify behavior in-game.
4. Clean up naming/comments/types.
5. Re-test key gameplay loop and screens.
6. Commit with a clear message.

## 16. Definition of Done

A change is complete when:

- Code is readable and follows conventions above.
- Behavior is verified in the running game.
- No avoidable per-frame inefficiencies were introduced.
- Related docs/constants were updated if needed.
