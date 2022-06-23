from re import sub
from nebula import db, create_app
from random import randrange
from datetime import timedelta
from nebula.models import User, Course, CourseLevel, Question, Comment, Answer, SubjectTag
from nebula.views.user import create_user

app = create_app()

app.app_context().push()

for column in [User, Course, CourseLevel, Question, Comment, Answer, SubjectTag]:
    column.query.delete()

db.session.commit()


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


course_levels = [
    CourseLevel(name="First Year", study_type="Bachelor", code="bsc-yr1"),
    CourseLevel(name="Second Year", study_type="Bachelor", code="bsc-yr2"),
    CourseLevel(name="Third Year", study_type="Bachelor", code="bsc-yr3"),
    CourseLevel(name="General", study_type="Master", code="msc"),
]

courses = [
    # First Year Bachelor
    Course(name="Mechanics and Relativity",
           code="WBPH001-10",
           description="This course addresses topics in special relativity and mechanics at varying levels of mathematical complexity.",
           course_level=course_levels[0],
           semester="1"),
    Course(name="Calculus 1",
           code="WBMA003-05",
           description="This course introduces the basic concepts of quantum mechanics and its application to the study of the universe.",
           course_level=course_levels[0],
           semester="1a"),
    Course(name="Physics Laboratory 1",
           code="WBPH013-05",
           description="",
           course_level=course_levels[0],
           semester="1a"),
    Course(name="Linear Algebra (for Physics)",
           code="WBPH054-05",
           description="Linear algebra is the branch of mathematics concerning linear equations.",
           course_level=course_levels[0],
           semester="1b"),
    Course(name="Introduction Astronomy",
           code="WBAS007-05",
           description="Magnitudes, methods to measure distances, black bodies, spectra of stars, Hertzsprung-Russell diagram, binary stars, methods to measure stellar masses, stellar structure and evolution, the interstellar medium, star formation, the Milky Way and other galaxies, large scale structure, cosmology/Big Bang, the Solar System",
           course_level=course_levels[0],
           semester="1b"),
    Course(name="Electricity and Magnetism",
           code="WBPH033-10",
           description="",
           course_level=course_levels[0],
           semester="2"),
    Course(name="Calculus 2",
           code="WBMA029-05",
           description="",
           course_level=course_levels[0],
           semester="2a"),
    Course(name="Introduction to Programming and Computational Methods",
           code="WBAS013-05",
           description="",
           course_level=course_levels[0],
           semester="2a"),
    Course(name="Mathematical Physics",
           code="WBPH049-05",
           description="",
           course_level=course_levels[0],
           semester="2b"),
    Course(name="Observational Astronomy",
           code="WBAS015-05",
           description="",
           course_level=course_levels[0],
           semester="2b"),


    # Second Year Bachelor
    Course(name="Thermal Physics",
           code="WBPH002-10",
           description="",
           course_level=course_levels[1],
           semester="1"),
    Course(name="Quantum Physics 1",
           code="WBPH014-05",
           description="",
           course_level=course_levels[1],
           semester="1a"),
    Course(name="Statistics for Astronomy",
           code="WBAS004-05",
           description="The objective of the course is to get an introduction into commonly used statistical methods in astronomy and to familiarize students with measurement errors. The course is focussed on the Bayesian approach to statistics, and starts with basic probability theory. The student is introduced to the estimation of single and multiple parameters from data. Several probability distribution functions are presented and their use is explained. The concepts of maximum likelihood, hypothesis testing, model selection and model fitting are covered, with emphasis on fitting data to a straight line.",
           course_level=course_levels[1],
           semester="1a"),
    Course(name="Complex Analysis",
           code="WBMA018-05",
           description="",
           course_level=course_levels[1],
           semester="1b"),
    Course(name="Waves and Optics",
           code="WBPH032-05",
           description="",
           course_level=course_levels[1],
           semester="1b"),
    Course(name="Numerical Methods",
           code="WBAS014-05",
           description="",
           course_level=course_levels[1],
           semester="2a"),
    Course(name="Physics, Astronomy & Society: Ethical & Professional Aspects",
           code="WBPH053-05",
           description="",
           course_level=course_levels[1],
           semester="2a"),
    Course(name="Structure of Matter 1",
           code="WBPH046-05",
           description="",
           course_level=course_levels[1],
           semester="2a"),
    Course(name="Physics of Galaxies",
           code="WBAS016-05",
           description="",
           course_level=course_levels[1],
           semester="2b"),
    Course(name="Physics of Stars",
           code="WBAS017-05",
           description="",
           course_level=course_levels[1],
           semester="2b"),
    Course(name="Quantum Physics 2",
           code="WBPH052-05",
           description="",
           course_level=course_levels[1],
           semester="2b"),

    # Third Year Bachelor
    Course(name="Astroparticle Physics",
           code="WBPH036-05",
           description="",
           course_level=course_levels[2],
           semester="2a"),
    Course(name="Astrophysical Hydrodynamics",
           code="WBAS011-05",
           description="",
           course_level=course_levels[2],
           semester="2a"),
    Course(name="Interstellar medium",
           code="WBAS012-05",
           description="",
           course_level=course_levels[2],
           semester="2a"),
    Course(name="Astronomy Bachelor Research Project",
           code="WBAS901-15",
           description="",
           course_level=course_levels[2],
           semester="2b"),

    # General Master
    Course(name="General Relativity",
           code="WMPH009-05",
           description="",
           course_level=course_levels[3],
           semester="1a"),
    Course(name="Introduction to Data Science",
           code="WMCS002-05",
           description="",
           course_level=course_levels[3],
           semester="1a"),
    Course(name="Electrodynamics of Radiation Processes",
           code="WMAS008-05",
           description="",
           course_level=course_levels[3],
           semester="1b"),
    Course(name="Particle Phyics Phenomenology",
           code="WMPH026-05",
           description="",
           course_level=course_levels[3],
           semester="2a"),
    Course(name="Student Seminar Quantum Universe",
           code="WMPH039-05",
           description="",
           course_level=course_levels[3],
           semester="2b")
]

db.session.add_all(course_levels)
db.session.commit()

users = [
    create_user("test_user", "unsafe", email="test_user1@nebula.com",
                access_level=1, first_name="Test", last_name="User1"),
    create_user("test_user2", "unsafe", email="test_user2@nebula.com",
                access_level=1, first_name="Test", last_name="User2"),
    create_user("test_moderator1", "unsafe", email="test_moderator1@nebula.com",
                access_level=2, first_name="Test", last_name="Moderator1"),
    create_user("test_moderator2", "unsafe", email="test_moderator2@nebula.com",
                access_level=2, first_name="Test", last_name="Moderator2"),
    create_user("test_admin", "unsafe", email="test_admin@nebula.com",
                access_level=3, first_name="Test", last_name="Admin"),

    create_user("pieterh", "unsafe", email="pieterh@nebula.com",
                access_level=3, first_name="Pieter", last_name="Huizenga"),
]

subject_tags = {
    "Astronomy":     SubjectTag(name="Astronomy"),
    "Astrophysics":  SubjectTag(name="Astrophysics"),
    "Computing":     SubjectTag(name="Computing"),
    "Earth Science": SubjectTag(name="Earth Science"),
    "Mathematics":   SubjectTag(name="Mathematics"),
    "Physics":       SubjectTag(name="Physics"),
    "Quantum Physics": SubjectTag(name="Quantum Physics"),
    "Statistics":    SubjectTag(name="Statistics")
}


print(users)
questions = [
    Question(title="What is the answer to life, the universe and everything?",
             content="How do you know?",
             course=courses[0],
             subject_tags=[subject_tags["Physics"]],
             reviewed=1,
             user=users[5]),
    Question(title="This is the first question",
             content="This is the first content",
             course=courses[0],
             subject_tags=[subject_tags["Mathematics"]],
             reviewed=1,
             user=users[5]),
    Question(title="This is the second question",
             content="This is the second content",
             course=courses[0],
             subject_tags=[subject_tags["Statistics"]],
             reviewed=2,
             user=users[5]),
    Question(title="This is the third question",
             content="This is the third content",
             course=courses[13],
             subject_tags=[subject_tags["Astronomy"],
                           subject_tags["Astrophysics"], subject_tags["Computing"]],
             reviewed=1,
             user=users[5]),
    Question(title="This is the fourth question",
             content="This is the fourth content",
             course=courses[0],
             subject_tags=[subject_tags["Earth Science"],
                           subject_tags["Mathematics"]],
             reviewed=2,
             user=users[3]),
    Question(title="This is the fifth question",
             content="This is the fifth content",
             course=courses[0],
             subject_tags=[subject_tags["Physics"],
                           subject_tags["Quantum Physics"]],
             reviewed=1,
             user=users[2]),
    Question(title="This is the sixth question",
             content="This is the sixth content",
             course=courses[0],
             subject_tags=[subject_tags["Physics"],
                           subject_tags["Quantum Physics"]],
             reviewed=1,
             user=users[1]),
    Question(title="This is the seventh question",
             content="This is the seventh content",
             course=courses[0],
             subject_tags=[subject_tags["Statistics"],
                           subject_tags["Quantum Physics"]],
             reviewed=1,
             user=users[0]),
    Question(title="This is the eighth question",
             content="This is the eighth content",
             course=courses[0],
             subject_tags=[subject_tags["Physics"]],
             reviewed=1,
             user=users[0]),
    Question(title="This is the ninth question",
             content="This is the ninth content",
             course=courses[0],
             subject_tags=[subject_tags["Physics"]],
             user=users[4]),
    Question(title="This is the tenth question",
             content="This is the tenth content",
             course=courses[1],
             subject_tags=[subject_tags["Astronomy"]],
             reviewed=1,
             user=users[1]),
    Question(title="This is the eleventh question",
             content="This is the eleventh content",
             course=courses[1],
             subject_tags=[subject_tags["Astronomy"]],
             user=users[0]),
    Question(title="This is the twelfth question",
             content="This is the twelfth content",
             course=courses[1],
             subject_tags=[subject_tags["Astronomy"]],
             user=users[4]),
    Question(title="This is the thirteenth question",
             content="This is the thirteenth content",
             course=courses[1],
             subject_tags=[subject_tags["Astronomy"]],
             user=users[0]),
    Question(title="This is the fourteenth question",
             content="This is the fourteenth content",
             course=courses[1],
             subject_tags=[subject_tags["Astronomy"]],
             user=users[3]),
    Question(title="This is the fifteenth question",
             content="This is the fifteenth content",
             course=courses[1],
             subject_tags=[subject_tags["Astronomy"]],
             user=users[2]),
    Question(title="This is the sixteenth question",
             content="This is the sixteenth content",
             course=courses[1],
             subject_tags=[subject_tags["Astronomy"]],
             user=users[4]),
    Question(title="This is the seventeenth question",
             content="This is the seventeenth content",
             course=courses[1],
             subject_tags=[subject_tags["Astronomy"]],
             user=users[1]),
    Question(title="This is the eighteenth question",
             content="This is the eighteenth content",
             course=courses[1],
             subject_tags=[subject_tags["Astronomy"]],
             user=users[3]),
    Question(title="This is the nineteenth question",
             content="This is the nineteenth content",
             course=courses[1],
             subject_tags=[subject_tags["Astronomy"]],
             reviewed=1,
             user=users[2]),
    Question(title="This is the twentieth question",
             content="This is the twentieth content",
             course=courses[1],
             subject_tags=[subject_tags["Astronomy"]],
             reviewed=1,
             user=users[4]),
    Question(title="This is the twenty-first question",
             content="This is the twenty-first content",
             course=courses[1],
             subject_tags=[subject_tags["Astronomy"]],
             user=users[0]),
    Question(title="How to use Markdown",
             content="""
             You will like those projects!

---

If you want to add Latex to your question, please use the following format:

For block equations, use `$$ equation $$`,  which will look like this:
$$ \\nabla f = [\\frac{\partial f}{\partial x} \hat{x} + \\frac{\partial
f}{\partial y} \hat{y} +\\frac{\partial f}{\partial z} \hat{z}] $$

For inline equations, use `$ equation $`, which will look like this: $ |\\vec{r}| = \sqrt{x^2 + y^2 + z^2} $

To use numbered equations, use 
```
\\begin{equation}\label{equation:quadruple-integral2} 
\iiiint_V \mu(t,u,v,w) \,dt\,du\,dv\,dw
\end{equation}
```
\\begin{equation}  \label{equation:quadruple-integral2}
\iiiint_V \mu(t,u,v,w) \,dt\,du\,dv\,dw
\end{equation}

---

# h1 Heading 8-)
## h2 Heading
### h3 Heading
#### h4 Heading
##### h5 Heading
###### h6 Heading

---

## Horizontal Rules

___

---

***

## Emphasis

**This is bold text**

__This is bold text__

*This is italic text*

_This is italic text_

~~Strikethrough~~


## Blockquotes


> Blockquotes can also be nested...
>> ...by using additional greater-than signs right next to each other...
> > > ...or with spaces between arrows.


## Lists

Unordered

+ Create a list by starting a line with `+`, `-`, or `*`
+ Sub-lists are made by indenting 2 spaces:
  - Marker character change forces new list start:
    * Ac tristique libero volutpat at
    + Facilisis in pretium nisl aliquet
    - Nulla volutpat aliquam velit
+ Very easy!

Ordered

1. Lorem ipsum dolor sit amet
2. Consectetur adipiscing elit
3. Integer molestie lorem at massa


1. You can use sequential numbers...
1. ...or keep all the numbers as `1.`

Start numbering with offset:

57. foo
1. bar


## Code

Inline `code`

Indented code

    // Some comments
    line 1 of code
    line 2 of code
    line 3 of code
    test


Block code "fences"

```
Sample text here...
```

Syntax highlighting

``` js
var foo = function (bar) {
  return bar++;
};

console.log(foo(5));
```

## Tables

| Option | Description |
| ------ | ----------- |
| data   | path to data files to supply the data that will be passed into templates. |
| engine | engine to be used for processing templates. Handlebars is the default. |
| ext    | extension to be used for dest files. |
| more rows | another column |

Right aligned columns

| Option | Description |
| ------:| -----------:|
| data   | path to data files to supply the data that will be passed into templates. |
| engine | engine to be used for processing templates. Handlebars is the default. |
| ext    | extension to be used for dest files. |


## Links

[link text](http://dev.nodeca.com)

[link with title](http://nodeca.github.io/pica/demo/ "title text!")

Autoconverted link https://github.com/nodeca/pica (enable linkify to see)


## Images

![Minion](https://octodex.github.com/images/minion.png)
![Stormtroopocat](https://octodex.github.com/images/stormtroopocat.jpg "The Stormtroopocat")

Like links, Images also have a footnote style syntax

![Alt text][id]

With a reference later in the document defining the URL location:

[id]: https://octodex.github.com/images/dojocat.jpg  "The Dojocat"


## Plugins

The killer feature of `markdown-it` is very effective support of
[syntax plugins](https://www.npmjs.org/browse/keyword/markdown-it-plugin).


### [Emojies](https://github.com/markdown-it/markdown-it-emoji)

> Classic markup: :wink: :crush: :cry: :tear: :laughing: :yum:
>
> Shortcuts (emoticons): :-) :-( 8-) ;)

see [how to change output](https://github.com/markdown-it/markdown-it-emoji#change-output) with twemoji.


### [Subscript](https://github.com/markdown-it/markdown-it-sub) / [Superscript](https://github.com/markdown-it/markdown-it-sup)

- 19^th^
- H~2~O


### [\<ins>](https://github.com/markdown-it/markdown-it-ins)

++Inserted text++


### [\<mark>](https://github.com/markdown-it/markdown-it-mark)

==Marked text==


### [Footnotes](https://github.com/markdown-it/markdown-it-footnote)

Footnote 1 link[^first].

Footnote 2 link[^second].

Inline footnote^[Text of inline footnote] definition.

Duplicated footnote reference[^second].

[^first]: Footnote **can have markup**

    and multiple paragraphs.

[^second]: Footnote text.


### [Definition lists](https://github.com/markdown-it/markdown-it-deflist)

Term 1

:   Definition 1
with lazy continuation.

Term 2 with *inline markup*

:   Definition 2

        { some code, part of Definition 2 }

    Third paragraph of definition 2.

_Compact style:_

Term 1
  ~ Definition 1

Term 2
  ~ Definition 2a
  ~ Definition 2b


### [Abbreviations](https://github.com/markdown-it/markdown-it-abbr)

This is HTML abbreviation example.

It converts "HTML", but keep intact partial entries like "xxxHTMLyyy" and so on.

*[HTML]: Hyper Text Markup Language

### [Custom containers](https://github.com/markdown-it/markdown-it-container)

::: warning
*here be dragons*
:::""",
             user=users[5],
             course=courses[0],
             reviewed=0,
             subject_tags=[SubjectTag(name="Markdown")])
]

Answers = [
    Answer(content="42",
           question=questions[0],
           sources=["https://www.google.com",
                    "https://www.wikipedia.org", "https://www.youtube.com"],
           user=users[5]),
    Answer(content="This is the first answer",
           question=questions[0],
           sources=["https://www.google.com",
                    "https://www.wikipedia.org", "https://rug.nl"],
           user=users[2]),
    Answer(content="This is the second answer",
           question=questions[0],
           sources=["https://www.google.com"],
           user=users[3]),
    Answer(content="This is the third answer",
           question=questions[1],
           sources=["https://www.google.com"],
           user=users[1]),
    Answer(content="This is the fourth answer",
           question=questions[2],
           sources=["https://www.google.com"],
           user=users[5]),
    Answer(content="This is the fifth answer",
           question=questions[3],
           sources=["https://www.google.com"],
           user=users[5]),
    Answer(content="This is the sixth answer",
           question=questions[3],
           sources=["https://www.google.com"],
           user=users[5]),
    Answer(content="This is the seventh answer",
           question=questions[3],
           sources=["https://www.google.com"],
           user=users[5]),
    Answer(content="This is the eighth answer",
           question=questions[3],
           user=users[5]),

]


comments = [
    Comment(content="This is the first comment",
            question=questions[0],
            user=users[5]),
    Comment(content="This is the second comment",
            question=questions[0],
            user=users[4]),
    Comment(content="This is the third comment",
            question=questions[0],
            user=users[2]),
    Comment(content="This is the fourth comment",
            question=questions[0],
            user=users[5])
]


db.session.add_all(users)


db.session.add_all(questions)

db.session.commit()
