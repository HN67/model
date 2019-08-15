# Model

A system to visualize mathematical models using Python and Pygame.

Implementation of a model is done by subclassing the base.Model class with a constructor and attributes representing model state, and implement the base.Model.visual() method to return a Pygame surface holding a visual representation of the model.

Also, usually the base.Manager class is subclassed to hook the Model to Pygame display and events to show output and allow interactivity.

An example implementation is the ```stargon``` module, which draws pointed stars. The implementation currently hooked to main is ```projection```, which projects a 3D environment onto the screen.

## Projection

| Dependencies |
|--------------|
| [pygame](https://www.pygame.org/wiki/GettingStarted) |
| [pyquaternion](http://kieranwynn.github.io/pyquaternion/) |

### Controls

Key | Action
-------|----
W | Pan Up
A | Pan Left
S | Pan Down
D | Pan Right
Q | Pan Out
E | Pan In
↑ | Look Up
← | Look Left
→ | Look Right
↓ | Look Down
< | Tilt Left
\> | Tilt Right
