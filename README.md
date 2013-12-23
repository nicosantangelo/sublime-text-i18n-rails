# Sublime Text: Rails I18n

This plugin is aimed to help you create Internationalization keys.

## Usage

### Adding keys

To add a key, go to a Rails view, select the key you want to add a value to and [run][1] the command "I18n Rails: Add key".
The plugin will display a prompt asking for the value in every language available, If the key value is found, the prompt will show it (so it can be edited easily).

The package supports relative and absolute routes, for example


````erb
<%# views/users/index.html.erb %>

<%= t('.hello') %>  <%# It will search in config/locales/views/users/*.yml (see note below) %>

<%# (...) %>

<%= t('some.other.key.bye') %> <%# It will search in config/locales/*.yml %>
````

**Note:** If the package doesn't find the path (for example with `.hello`) it will default to `config/locales/*.yml`

### Checking keys
If you want to check which keys in the file are present in the `*.yml` files, you can open up a Rails view and [run][1] "I18n Rails: Toggle key highlighting", resulting in something like this:

![](https://raw.github.com/NicoSantangelo/sublime-text-i18n-rails/master/demo.png)

Each translation is looked up in the relative or absolute path (the same logic applied for adding the values). So, in the example:
  
  * `.missing_key` wasn't found on any `*.yml` file. Uses the "invalid" scope for the color.
  * `.partial` was found in some locales but no all (for example, only defined in en.yml but missing in es.yml). Uses the "string" scope for the color.
  * `.full` is correctly added. Uses the "comment" scope for the color.


## Shortcut Keys

**Windows and Linux:**

 * Add:   `ctrl+alt+i` 
 * Toggle: `ctrl+alt+u`

**OSX**

 * Add:   `super+alt+i` 
 * Toggle: `super+alt+u` 

## Installation

This package is available in [Package Control][2] or you can clone the repo into your package folder (use Package Control, is awesome).

## Roadmap

 * Command to "Go to yml file".
 * Support custom color scopes.
 * Allow path filtering.

## License
[MIT][3]

  [1]: https://github.com/NicoSantangelo/sublime-text-i18n-rails#shortcut-keys
  [2]: https://sublime.wbond.net/
  [3]: https://raw.github.com/NicoSantangelo/sublime-text-i18n-rails/master/LICENSE