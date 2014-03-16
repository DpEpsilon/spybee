Simple PYthon Blogging EnginE
=============================

### Built on the bottle.py web framework. ###

Writing Posts
-------------

Blog posts are placed in the 'posts' folder and are written in markdown.
For a blog post to be displayed, there needs to be a '<name>.json' file and
a '<name>.md' file. The json file needs to have a 'timestamp' (which is a unix
timetstamp) and optionally, a list of 'tags'. Tags currently serve no purpose,
but in the future, they may be used for bucketing posts together.

Customization
-------------

You can change what the homepage says by editing home.md. If this file does
not exist or markdown causes an error for whatever reason, nothing will be
shown on the homepage.

Dependencies
------------

Depends on python-argparse, python-markdown and python-json. By
default, spybee also uses python-paste as an alternate webserver so
that multi-threading is possible, but this isn't hard to change using
bottle.

Running
-------

Run with 'python main.py'. Use '-p' to specify port and '-d' to turn on
debug mode.

Future plans
------------
- Title and footer customization
- Tag filtering
- RSS

    Copyright Ⓒ 2013 Daniel Phillips

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
        http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.