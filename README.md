# Model

A system to visualize mathematical models using Python and Pygame.

Implementation of a model is done by subclassing the base.Model class with a constructor and attributes representing model state, and implement the base.Model.visual() method to return a Pygame surface holding a visual representation of the model.

Also, usually the base.Manager class is subclassed to hook the Model to Pygame display and events to show output and allow interactivity.

An example implementation is the ```stargon``` module, which is currently the module hooked to main.
