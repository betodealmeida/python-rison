# rison, a Python encoder/decoder for Rison

## Quickstart

```bash
$ pip install rison
```

```python
>>> import rison
>>> rison.dumps({'foo': 'bar'})
'(foo:bar)'
>>> rison.loads('(foo:bar)')
{'foo': 'bar'}
```

## Rison - Compact Data in URIs

This page describes *Rison*, a data serialization format optimized for compactness in URIs. Rison is a slight variation of JSON that looks vastly superior after URI encoding. Rison still expresses exactly the same set of data structures as JSON, so data can be translated back and forth without loss or guesswork. 

You can skip straight to some [examples](#examples), or read on for more background. 

### Why another data serialization format?

Rison is intended to meet the following goals, in roughly this order:

- Comply with [URI specifications](http://gbiv.com/protocols/uri/rfc/rfc3986.html) and usage
- Express **nested** data structures
- Be **human-readable**
- Be **compact**

Rison is necessary because the obvious alternatives fail to meet these goals:

- URI-encoded XML and JSON are illegible and inefficient.
- [HTML Form encoding](http://www.w3.org/TR/html4/interact/forms.html#form-content-type) rules the web but can only represent a flat list of string pairs.
- Ian Bicking's [FormEncode](http://formencode.org/) package includes the [variabledecode](http://formencode.org/Validator.html#id16) parser, an interesting convention for form encoding that allows nested lists and dictionaries. However, it becomes inefficient with deeper nesting, and allows no terminal datatypes except strings.

Note that these goals are shaped almost entirely by the constraints of URIs, though Rison has turned out to be useful in command-line tools as well. In the *body* of an HTTP request or response, length is less critical and URI encoding can be avoided, so JSON would usually be preferred to Rison.

Given that a new syntax is needed, Rison tries to innovate as little as possible:

- It uses the same data model as, and a very similar syntax to [JSON](http://json.org/). The Rison grammar is only a slight alteration of the JSON grammar.
- It introduces very little additional quoting, since we assume that URI encoding will be applied on top of the Rison encoding.

### Differences from JSON syntax

  * no whitespace is permitted except inside quoted strings. 
  * almost all character escaping is left to the uri encoder. 
  * single-quotes are used for quoting, but quotes can and should be left off strings when the strings are simple identifiers. 
  * the `e+` exponent format is forbidden, since `+` is not safe in form values and the plain `e` format is equivalent. 
  * the `E`, `E+`, and `E` exponent formats are removed. 
  * object keys should be lexically sorted when encoding. the intent is to improve url cacheability. 
  * uri-safe tokens are used in place of the standard json tokens: 
    
    |rison token|json token|meaning      |
    |:----------|:---------|:------------|
    |`'`        |`"`       |string quote |
    |`!`        |`\`       |string escape|
    |`(...)`    |`{...}`   |object       |
    |`!(...)`   |`[...]`   |array        |
    
  * the JSON literals that look like identifiers (`true`, `false` and `null`) are represented as `!` sequences: 
    
    |rison token|json token|
    |:----------|:---------|
    |`!t`       |`true`    |
    |`!f`       |`false`   |
    |`!n`       |`null`    |

The `!` character plays two similar but different roles, as an escape character within strings, and as a marker for special values. This may be confusing.

Notice that services can distinguish Rison-encoded strings from JSON-encoded strings by checking the first character. Rison structures start with `(` or `!(`. JSON structures start with `[` or `{`. This means that a service which expects a JSON encoded object or array can accept Rison-encoded objects without loss of compatibility.

### Interaction with URI %-encoding

Rison syntax is designed to produce strings that be legible after being [form-encoded](http://www.w3.org/TR/html4/interact/forms.html#form-content-type) for the [query](http://gbiv.com/protocols/uri/rfc/rfc3986.html#query) section of a URI. None of the characters in the Rison syntax need to be URI encoded in that context, though the data itself may require URI encoding. Rison tries to be orthogonal to the %-encoding process - it just defines a string format that should survive %-encoding with very little bloat. Rison quoting is only applied when necessary to quote characters that might otherwise be interpreted as special syntax.

Note that most URI encoding libraries are very conservative, percent-encoding many characters that are legal according to [RFC
3986](http://gbiv.com/protocols/uri/rfc/rfc3986.html). For example, Javascript's builtin `encodeURIComponent()` function will still make Rison strings difficult to read. The rison.js library includes a more tolerant URI encoder.

Rison uses its own quoting for strings, using the single quote (**`'`**) as a string delimiter and the exclamation point (**`!`**) as the string escape character. Both of these characters are legal in uris. Rison quoting is largely inspired by Unix shell command line parsing.

All Unicode characters other than **`'`** and **`!`** are legal inside quoted strings. This includes newlines and control characters. Quoting all such characters is left to the %-encoding process.

### Interaction with IRIs

This still needs to be addressed. Advice from an IRI expert would be very welcome.

Particular attention should be paid to Unicode characters that may be interpreted as Rison syntax characters.

The *idchars* set is hard to define well. The goal is to include foreign language alphanumeric characters and some punctuation that is common in identifiers (`_`, `-`, `.`, `/`, and others). However, whitespace and most punctuation characters should require quoting. 

### Emailing URIs

Most text emailers are conservative about what they turn into a hyperlink, and they will assume that characters like `(` mean the end of the URI. This results in broken, truncated links.

This is actually a problem with URI encoding rather than with Rison, but it comes up a lot in practice. You could use Rison with a more aggressive URI encoder to generate emailable URIs. You can also wrap your emailed URIs in angle brackets: `<http://...>` which some mail readers have better luck with.

### Further Rationale

**Passing data in URIs** is necessary in many situations. Many web services rely on the HTTP GET method, which can take advantage of an extensive deployed caching infrastructure. Browsers also have different capabilities for GET, including the crucial ability to make cross-site requests. It is also very convenient to store the state of a small browser application in the URI.

**Human readability** makes everything go faster. Primarily this means avoiding URI encoding whenever possible. This requires careful choice of characters for the syntax, and a tolerant URI encoder that only encodes characters when absolutely necessary.

**Compactness** is important because of implementation limits on URI length. Internet Explorer is once again the weakest link at 2K. One could certainly invent a more compact representation by dropping the human-readable constraint and using a compression algorithm.

### Variations

There are several variations on Rison which are useful or at least thought-provoking. 

#### O-Rison

When you know the parameter being encoded will always be an object, always wrapping it in a containing `()` is unnecessary and hard to explain. Until you've dealt with nested structures, the need for parentheses is hard to explain. In this case you may wish to declare that the argument is encoded in *O-Rison*, which can be translated to Rison by wrapping it in parentheses.

Here's a URI with a single query argument which is a nested structure: `http://example.com/service?query=(q:'*',start:10,count:10)`

This is more legible if you specify that the argument is O-Rison instead of Rison, and leave the containing `()` as implied: `http://example.com/service?query=q:'*',start:10,count:10`

This seems to be useful in enough situations that it is worth defining the term *O-Rison*.

#### A-Rison

Similarly, sometimes you know the value will always be an array. Instead of specifying a Rison argument: `.../?items=!(item1,item2,item3)` you can specify the far more legible A-Rison argument: `.../?items=item1,item2,item3`

#### Accepting other delimiters

Notice that O-Rison looks almost like a drop-in replacement for [URL form encoding](http://www.w3.org/TR/html4/interact/forms.html#form-content-type), with two substitutions:

- `:` for `=`
- `,` for `&`

We could expand the Rison parser to treat all of `,`, `&`, and `;` as valid item separators and both `:` and `=` as key-value separators. In this case the vast majority of URI queries would form a flat subset of O-Rison. The exceptions are services that depend on ordering of query parameters or allow duplicate parameter names.

This extension doesn't change the parsing of standard Rison strings because `&`, `=`, and `;` are already illegal in Rison identifiers. 

### Examples

These examples compare Rison and JSON representations of identical values.

| Rison | JSON | URI-encoded Rison | URI-encoded JSON | Roundtrip test | Compression |
| --- | --- | --- | --- | --- | --- |
| `(a:0,b:1)` | `{"a": 0, "b": 1}` | `(a:0,b:1)` | `%7B%22a%22:+0,+%22b%22:+1%7D` | ok | 67.86% |
| `(a:0,b:foo,c:'23skidoo')` | `{"a": 0, "b": "foo", "c": "23skidoo"}` | `(a:0,b:foo,c:'23skidoo')` | `%7B%22a%22:+0,+%22b%22:+%22foo%22,+%22c%22:+%2223skidoo%22%7D` | ok | 60.66% |
| `!t` | `true` | `!t` | `true` | ok | 50.00% |
| `1.5` | `1.5` | `1.5` | `1.5` | ok | 0.00% |
| `-3` | `-3` | `-3` | `-3` | ok | 0.00% |
| `1e30` | `1e+30` | `1e30` | `1e%2B30` | ok | 42.86% |
| `1e-30` | `1e-30` | `1e-30` | `1e-30` | ok | 0.00% |
| `a` | `"a"` | `a` | `%22a%22` | ok | 85.71% |
| `'0a'` | `"0a"` | `'0a'` | `%220a%22` | ok | 50.00% |
| `'abc def'` | `"abc def"` | `%27abc+def%27` | `%22abc+def%22` | ok | 0.00% |
| `(a:0)` | `{"a": 0}` | `(a:0)` | `%7B%22a%22:+0%7D` | ok | 68.75% |
| `(id:!n,type:/common/document)` | `{"id": null, "type": "/common/document"}` | `(id:!n,type:/common/document)` | `%7B%22id%22:+null,+%22type%22:+%22/common/document%22%7D` | ok | 48.21% |
| `!(!t,!f,!n,'')` | `[true, false, null, ""]` | `!(!t,!f,!n,'')` | `%5Btrue,+false,+null,+%22%22%5D` | ok | 54.84% |
| `'-h'` | `"-h"` | `'-h'` | `%22-h%22` | ok | 50.00% |
| `a-z` | `"a-z"` | `a-z` | `%22a-z%22` | ok | 66.67% |
| `'wow!!'` | `"wow!"` | `'wow!!'` | `%22wow%21%22` | ok | 41.67% |
| `domain.com` | `"domain.com"` | `domain.com` | `%22domain.com%22` | ok | 37.50% |
| `'user@domain.com'` | `"user@domain.com"` | `'user@domain.com'` | `%22user@domain.com%22` | ok | 19.05% |
| `'US $10'` | `"US $10"` | `%27US+$10%27` | `%22US+$10%22` | ok | 0.00% |
| `'can!'t'` | `"can't"` | `'can!'t'` | `%22can%27t%22` | ok | 38.46% |
| `'Control-F: '` | `"Control-F: \u0006"` | `%27Control-F:+%06%27` | `%22Control-F:+%5Cu0006%22` | ok | 20.00% |
| `'Unicode: ௫'` | `"Unicode: \u0beb"` | `%27Unicode:+%E0%AF%AB%27` | `%22Unicode:+%5Cu0beb%22` | ok | -4.35% |

The compression ratio column shows (1 - encoded_rison_size / encoded_json_size).

On a log of Freebase mqlread service URIs, the queries were from 35% to 45% smaller when encoded with Rison.

URI encoding is done with a custom URI encoder which is less aggressive than Javascript's built-in `encodeURIComponent()`. 

### Grammar

Modified from the [json.org](https://web.archive.org/web/20130910064110/http://json.org/) grammar.

- _object_
  - `()`
  - `(` _members_ `)`
- _members_
  - _pair_
  - _pair_ `,` _members_
- _pair_
  - _key_ `:` _value_
- _array_
  - `!()`
  - `!(` _elements_ `)`
- _elements_
  - _value_
  - _value_ `,` _elements_
- _key_
  - _id_
  - _string_
- _value_
  - _id_
  - _string_
  - _number_
  - _object_
  - _array_
  - `!t`
  - `!f`
  - `!n`
    <br>
    　　　　────────────
- _id_
  - _idstart_
  - _idstart_ _idchars_
- _idchars_
  - _idchar_
  - _idchar_ _idchars_
- _idchar_
  - any alphanumeric ASCII character
  - any ASCII character from the set `-` `_` `.` `/` `~`
  - any non-ASCII Unicode character
- _idstart_
  - any _idchar_ not in `-`, _digit_
    <br>
    　　　　────────────
- _string_
  - `''`
  - `'` _strchars_ `'`
- _strchars_
  - _strchar_
  - _strchar_ _strchars_
- _strchar_
  - any Unicode character except ASCII `'` and `!`
  - `!!`
  - `!'`
    <br>
    　　　　────────────
- _number_
  - _int_
  - _int_ _frac_
  - _int_ _exp_
  - _int_ _frac_ _exp_
- _int_
  - _digit_
  - _digit1-9_ _digits_
  - `-` digit
  - `-` digit1-9 digits
- _frac_
  - `.` _digits_
- _exp_
  - _e_ _digits_
- _digits_
  - _digit_
  - _digit_ _digits_
- _e_
  - `e`
  - `e-`

## History

Rison original website is now dead. You can find an archive [here](https://web.archive.org/web/20130910064110/http://www.mjtemplate.org/examples/rison.html).

This package was originally forked from https://github.com/pifantastic/python-rison and published to PyPI as "prison" (Python + Rison) because the "rison" name was taken. Starting with version 2.0.0, the package has been renamed to "rison", modernized for Python 3.10+, and all Python 2 dependencies have been removed.
