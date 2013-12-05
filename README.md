# Sublime Text: Rails I18n

This plugin is aimed to help you create Internationalization keys.

## Usage
To use the plugin, go to a Rails view select the key where you want to add a value to and [run][1] the command "I18n Rails: Add key".
The plugin will display a prompt asking for the value in every language available.

The plugin supports relative and absolute routes, for example


````erb
<%# views/users/index.html.erb %>

<%= t('.hello') %>  <%# It will search in config/locales/views/users/*.yml (see note below) %>

<%# (...) %>

<%= t('some.other.key.bye') %> <%# It will search in config/locales/*.yml %>
````

**Note:** If the plugin doesn't find the path (for example with `.hello`) it will default to `config/locales/*.yml`

## Shortcut Keys

**Windows or Linux:**

 * `ctrl+alt+i` 

**OSX**

 * `super+alt+i` 

## Installation

This package is available in [Package Control][2] or you can clone the repo into your package folder (use Package Control, is awesome).

## License
[MIT][3]

  [1]: https://github.com/NicoSantangelo/sublime-text-i18n-rails#shortcut-keys
  [2]: https://sublime.wbond.net/
  [3]: https://raw.github.com/NicoSantangelo/sublime-text-i18n-rails/master/LICENSE