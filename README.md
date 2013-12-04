# Sublime Text: Rails I18n

This plugin is aimed to help you create Internationalization keys.

## Usage
To use the plugin, go to a Rails view select the key where you want to add a value to and [run][1] the command "I18n Rails: Add key".
The plugin will display a prompt asking for the value in every language available.

The plugin supports relative and absolute routes, for example


````erb
<%# views/users/index.html.erb %>

<%= t('.hello') %>  <%# It will search in config/locales/views/users/*.yml %>

<%# (...) %>

<%= t('some.other.key.bye') %> <%# It will search in config/locales/*.yml %>
````

Right now the plugin wont create a missing file or folder, and the relative path is fixed, but the idea [is making this configurable][2].

## Shortcut Keys

**Windows or Linux:**

 * `ctrl+alt+i` 

**OSX**

 * `super+alt+i` 

## Installation

This package is available in [Package Control][3] or you can clone the repo into your package folder (use Package Control, is awesome).

## Roadmap
 - Setting to create missing files
 - Setting to configure the default relative path

## License
[MIT][4]

  [1]: https://github.com/NicoSantangelo/sublime-text-i18n-rails#shortcut-keys
  [2]: https://github.com/NicoSantangelo/sublime-text-i18n-rails#roadmap
  [3]: https://sublime.wbond.net/
  [4]: https://raw.github.com/NicoSantangelo/sublime-text-i18n-rails/master/LICENSE