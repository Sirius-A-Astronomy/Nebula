# Project Structure

Nebula uses a [Flask](https://flask.palletsprojects.com/en/2.0.x/) backend and a [Vite](https://vitejs.dev/) + [Vue](https://vuejs.org/) frontend. The project structure is as follows:

```
📂docs
📂nebula
 ┣ 📂cli
 ┣ 📂models
 ┣ 📂routes
 ┣ 📂src
 ┣ 📂static
 ┣ 📂templates
 ┣ 📂helpers
 ┣ 📜__init__.py
📜config.py
...
```

```
📦nebula
 ┣ 📂cli
 ┃ ┣ 📜db.py
 ┃ ┗ 📜user.py
 ┣ 📂helpers
 ┃ ┣ 📜access_levels.py
 ┃ ┣ 📜error_bin.py
 ┃ ┣ 📜error_handler.py
 ┃ ┣ 📜global_functions.py
 ┃ ┗ 📜unauthorized_handler.py
 ┣ 📂models
 ┃ ┣ 📜answer.py
 ┃ ┣ 📜comment.py
 ┃ ┣ 📜course.py
 ┃ ┣ 📜course_level.py
 ┃ ┣ 📜notification.py
 ┃ ┣ 📜question.py
 ┃ ┣ 📜subject_tag.py
 ┃ ┣ 📜subscription.py
 ┃ ┣ 📜user.py
 ┃ ┗ 📜__init__.py
 ┣ 📂routes
 ┃ ┣ 📂api
 ┃ ┃ ┣ 📜answer_api.py
 ┃ ┃ ┣ 📜api.py
 ┃ ┃ ┣ 📜comment_api.py
 ┃ ┃ ┣ 📜courses_api.py
 ┃ ┃ ┣ 📜course_level_api.py
 ┃ ┃ ┣ 📜question_api.py
 ┃ ┃ ┣ 📜search_api.py
 ┃ ┃ ┣ 📜session_api.py
 ┃ ┃ ┣ 📜subject_tag_api.py
 ┃ ┃ ┣ 📜user_api.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂web
 ┃ ┃ ┣ 📜add_question.py
 ┃ ┃ ┣ 📜all_courses.py
 ┃ ┃ ┣ 📜course.py
 ┃ ┃ ┣ 📜dashboard.py
 ┃ ┃ ┣ 📜documentation.py
 ┃ ┃ ┣ 📜errors.py
 ┃ ┃ ┣ 📜level.py
 ┃ ┃ ┣ 📜main.py
 ┃ ┃ ┣ 📜question.py
 ┃ ┃ ┣ 📜search.py
 ┃ ┃ ┣ 📜user.py
 ┃ ┃ ┗ 📜__init__.py
 ┣ 📂src
 ┃ ┣ 📂js
 ┃ ┃ ┣ 📂components
 ┃ ┃ ┃ ┣ 📂baseLayout
 ┃ ┃ ┃ ┃ ┣ 📜BaseHeader.vue
 ┃ ┃ ┃ ┃ ┣ 📜DropdownMenu.vue
 ┃ ┃ ┃ ┃ ┣ 📜mobileNavMenu.vue
 ┃ ┃ ┃ ┃ ┣ 📜NavDropdown.vue
 ┃ ┃ ┃ ┃ ┗ 📜recursiveMobileNavDropdown.vue
 ┃ ┃ ┃ ┣ 📂course
 ┃ ┃ ┃ ┃ ┗ 📜CourseForm.vue
 ┃ ┃ ┃ ┣ 📂courseLevel
 ┃ ┃ ┃ ┃ ┗ 📜CourseLevelForm.vue
 ┃ ┃ ┃ ┣ 📂dashboard
 ┃ ┃ ┃ ┃ ┣ 📜DashboardHeader.vue
 ┃ ┃ ┃ ┃ ┗ 📜DashboardSidemenu.vue
 ┃ ┃ ┃ ┣ 📂global_search
 ┃ ┃ ┃ ┃ ┣ 📜GlobalSearch.vue
 ┃ ┃ ┃ ┃ ┣ 📜GlobalSearchResults.vue
 ┃ ┃ ┃ ┃ ┗ 📜HighlightResult.vue
 ┃ ┃ ┃ ┣ 📂icons
 ┃ ┃ ┃ ┃ ┣ 📜ArrowBack.vue
 ┃ ┃ ┃ ┃ ┣ 📜CloseIcon.vue
 ┃ ┃ ┃ ┃ ┗ 📜InfoIcon.vue
 ┃ ┃ ┃ ┣ 📂question
 ┃ ┃ ┃ ┃ ┣ 📜AnswerShow.vue
 ┃ ┃ ┃ ┃ ┣ 📜CommentShow.vue
 ┃ ┃ ┃ ┃ ┣ 📜EditAnswer.vue
 ┃ ┃ ┃ ┃ ┣ 📜QuestionEditor.vue
 ┃ ┃ ┃ ┃ ┣ 📜QuestionForm.vue
 ┃ ┃ ┃ ┃ ┗ 📜QuestionListItem.vue
 ┃ ┃ ┃ ┣ 📂subjectTag
 ┃ ┃ ┃ ┃ ┣ 📜RemovableSubjectTag.vue
 ┃ ┃ ┃ ┃ ┣ 📜SubjectTag.vue
 ┃ ┃ ┃ ┃ ┗ 📜SubjectTagEditor.vue
 ┃ ┃ ┃ ┣ 📂ui
 ┃ ┃ ┃ ┃ ┣ 📂modals
 ┃ ┃ ┃ ┃ ┃ ┗ 📜ModalContainer.vue
 ┃ ┃ ┃ ┃ ┣ 📜CookieNotice.vue
 ┃ ┃ ┃ ┃ ┗ 📜FlashContainer.vue
 ┃ ┃ ┃ ┣ 📂user
 ┃ ┃ ┃ ┃ ┣ 📜UserForm.vue
 ┃ ┃ ┃ ┃ ┗ 📜userValidation.ts
 ┃ ┃ ┃ ┣ 📜BreadCrumbs.vue
 ┃ ┃ ┃ ┣ 📜MarkdownDisplay.vue
 ┃ ┃ ┃ ┣ 📜MarkdownEditor.vue
 ┃ ┃ ┃ ┗ 📜TheDarkModeToggle.vue
 ┃ ┃ ┣ 📂http
 ┃ ┃ ┃ ┗ 📜api.ts
 ┃ ┃ ┣ 📂lib
 ┃ ┃ ┃ ┣ 📜highlighter.ts
 ┃ ┃ ┃ ┣ 📜mathjax.ts
 ┃ ┃ ┃ ┗ 📜permissionHelpers.ts
 ┃ ┃ ┣ 📂router
 ┃ ┃ ┃ ┣ 📜baseRoutes.ts
 ┃ ┃ ┃ ┣ 📜courseRoutes.ts
 ┃ ┃ ┃ ┣ 📜index.ts
 ┃ ┃ ┃ ┣ 📜questionRoutes.ts
 ┃ ┃ ┃ ┗ 📜userRoutes.ts
 ┃ ┃ ┣ 📂stores
 ┃ ┃ ┃ ┣ 📂factory
 ┃ ┃ ┃ ┃ ┗ 📜storeFactory.ts
 ┃ ┃ ┃ ┣ 📜appState.ts
 ┃ ┃ ┃ ┣ 📜courseLevelStore.ts
 ┃ ┃ ┃ ┣ 📜courseStore.ts
 ┃ ┃ ┃ ┣ 📜dashboardStore.ts
 ┃ ┃ ┃ ┣ 📜flashStore.ts
 ┃ ┃ ┃ ┣ 📜modalStore.ts
 ┃ ┃ ┃ ┣ 📜questionStore.ts
 ┃ ┃ ┃ ┣ 📜sessionStore.ts
 ┃ ┃ ┃ ┣ 📜subjectTagStore.ts
 ┃ ┃ ┃ ┗ 📜userStore.ts
 ┃ ┃ ┣ 📂views
 ┃ ┃ ┃ ┣ 📂course
 ┃ ┃ ┃ ┃ ┣ 📂components
 ┃ ┃ ┃ ┃ ┃ ┣ 📜CourseLevelListItem.vue
 ┃ ┃ ┃ ┃ ┃ ┗ 📜CourseListItem.vue
 ┃ ┃ ┃ ┃ ┣ 📜CourseIndex.vue
 ┃ ┃ ┃ ┃ ┣ 📜CourseShow.vue
 ┃ ┃ ┃ ┃ ┗ 📜LevelShow.vue
 ┃ ┃ ┃ ┣ 📂dashboard
 ┃ ┃ ┃ ┃ ┣ 📂courseLevels
 ┃ ┃ ┃ ┃ ┃ ┗ 📜CourseLevelShow.vue
 ┃ ┃ ┃ ┃ ┣ 📂courses
 ┃ ┃ ┃ ┃ ┃ ┣ 📂components
 ┃ ┃ ┃ ┃ ┃ ┃ ┗ 📜courseLevel.vue
 ┃ ┃ ┃ ┃ ┃ ┣ 📜CourseCreate.vue
 ┃ ┃ ┃ ┃ ┃ ┣ 📜CourseIndex.vue
 ┃ ┃ ┃ ┃ ┃ ┗ 📜CourseShow.vue
 ┃ ┃ ┃ ┃ ┣ 📂questions
 ┃ ┃ ┃ ┃ ┃ ┣ 📜QuestionCreate.vue
 ┃ ┃ ┃ ┃ ┃ ┣ 📜QuestionIndex.vue
 ┃ ┃ ┃ ┃ ┃ ┗ 📜QuestionShow.vue
 ┃ ┃ ┃ ┃ ┗ 📂users
 ┃ ┃ ┃ ┃ ┃ ┣ 📜UserCreate.vue
 ┃ ┃ ┃ ┃ ┃ ┣ 📜UserIndex.vue
 ┃ ┃ ┃ ┃ ┃ ┗ 📜UserShow.vue
 ┃ ┃ ┃ ┣ 📂main
 ┃ ┃ ┃ ┃ ┗ 📜IndexView.vue
 ┃ ┃ ┃ ┣ 📂question
 ┃ ┃ ┃ ┃ ┣ 📜QuestionEditCreate.vue
 ┃ ┃ ┃ ┃ ┗ 📜QuestionShow.vue
 ┃ ┃ ┃ ┗ 📂user
 ┃ ┃ ┃ ┃ ┣ 📜LoginView.vue
 ┃ ┃ ┃ ┃ ┣ 📜ProfileEdit.vue
 ┃ ┃ ┃ ┃ ┗ 📜ProfileView.vue
 ┃ ┃ ┣ 📂vue-services
 ┃ ┃ ┃ ┗ 📂directives
 ┃ ┃ ┃ ┃ ┣ 📜clickOutside.ts
 ┃ ┃ ┃ ┃ ┗ 📜keydownEscape.ts
 ┃ ┃ ┣ 📜App.ts
 ┃ ┃ ┣ 📜App.vue
 ┃ ┃ ┣ 📜BaseLayout.vue
 ┃ ┃ ┣ 📜DashboardLayout.vue
 ┃ ┃ ┣ 📜global.d.ts
 ┃ ┃ ┗ 📜types.ts
 ┃ ┣ 📂public
 ┃ ┃ ┣ 📂fonts
 ┃ ┃ ┃ ┣ 📜lato-v20-latin-ext_latin-300.woff
 ┃ ┃ ┃ ┣ 📜lato-v20-latin-ext_latin-300.woff2
 ┃ ┃ ┃ ┣ 📜lato-v20-latin-ext_latin-300italic.woff
 ┃ ┃ ┃ ┣ 📜lato-v20-latin-ext_latin-300italic.woff2
 ┃ ┃ ┃ ┣ 📜lato-v20-latin-ext_latin-italic.woff
 ┃ ┃ ┃ ┣ 📜lato-v20-latin-ext_latin-italic.woff2
 ┃ ┃ ┃ ┣ 📜lato-v20-latin-ext_latin-regular.woff
 ┃ ┃ ┃ ┗ 📜lato-v20-latin-ext_latin-regular.woff2
 ┃ ┃ ┣ 📂images
 ┃ ┃ ┃ ┣ 📜login.svg
 ┃ ┃ ┃ ┣ 📜logo.svg
 ┃ ┃ ┃ ┣ 📜mark.svg
 ┃ ┃ ┃ ┣ 📜online-test.svg
 ┃ ┃ ┃ ┣ 📜profile.svg
 ┃ ┃ ┃ ┣ 📜register.svg
 ┃ ┃ ┃ ┣ 📜search.svg
 ┃ ┃ ┃ ┣ 📜siriuswebheader.png
 ┃ ┃ ┃ ┣ 📜stars.webp
 ┃ ┃ ┃ ┗ 📜twinkling.webp
 ┃ ┃ ┗ 📂js
 ┃ ┃ ┃ ┣ 📜darkmode.js
 ┃ ┃ ┃ ┣ 📜login-register.js
 ┃ ┃ ┃ ┣ 📜markdown-it.min.js
 ┃ ┃ ┃ ┣ 📜mathjax-config.js
 ┃ ┃ ┃ ┣ 📜navbar_submenu.js
 ┃ ┃ ┃ ┣ 📜notifications.js
 ┃ ┃ ┃ ┣ 📜pageloadanim.js
 ┃ ┃ ┃ ┣ 📜purify.min.js
 ┃ ┃ ┃ ┣ 📜purify.min.js.map
 ┃ ┃ ┃ ┣ 📜search.js
 ┃ ┃ ┃ ┣ 📜search_through_course.js
 ┃ ┃ ┃ ┣ 📜stoppageloadanim.js
 ┃ ┃ ┃ ┣ 📜tag_input.js
 ┃ ┃ ┃ ┗ 📜views.js
 ┃ ┣ 📂scss
 ┃ ┃ ┣ 📂abstracts
 ┃ ┃ ┃ ┣ 📜_colors.scss
 ┃ ┃ ┃ ┣ 📜_index.scss
 ┃ ┃ ┃ ┣ 📜_mixins.scss
 ┃ ┃ ┃ ┗ 📜_spacing.scss
 ┃ ┃ ┣ 📂backgrounds
 ┃ ┃ ┃ ┗ 📜stars.scss
 ┃ ┃ ┣ 📂components
 ┃ ┃ ┃ ┣ 📜forms.scss
 ┃ ┃ ┃ ┣ 📜_buttons.scss
 ┃ ┃ ┃ ┣ 📜_index.scss
 ┃ ┃ ┃ ┗ 📜_skeleton.scss
 ┃ ┃ ┗ 📜main.scss
 ┃ ┗ 📂scss_old
 ┃ ┃ ┣ 📂abstracts
 ┃ ┃ ┃ ┣ 📜_index.scss
 ┃ ┃ ┃ ┗ 📜_typography.scss
 ┃ ┃ ┣ 📂components
 ┃ ┃ ┃ ┣ 📜_alerts.scss
 ┃ ┃ ┃ ┣ 📜_cards.scss
 ┃ ┃ ┃ ┣ 📜_course-list.scss
 ┃ ┃ ┃ ┣ 📜_forms.scss
 ┃ ┃ ┃ ┣ 📜_index.scss
 ┃ ┃ ┃ ┣ 📜_loader.scss
 ┃ ┃ ┃ ┣ 📜_markdown.scss
 ┃ ┃ ┃ ┣ 📜_navigation.scss
 ┃ ┃ ┃ ┣ 📜_question-list.scss
 ┃ ┃ ┃ ┣ 📜_search-bar.scss
 ┃ ┃ ┃ ┗ 📜_tags.scss
 ┃ ┃ ┣ 📂mixins
 ┃ ┃ ┃ ┗ 📜_index.scss
 ┃ ┃ ┣ 📂views
 ┃ ┃ ┃ ┣ 📜course.scss
 ┃ ┃ ┃ ┣ 📜dashboard.scss
 ┃ ┃ ┃ ┣ 📜login_register.scss
 ┃ ┃ ┃ ┣ 📜profile.scss
 ┃ ┃ ┃ ┗ 📜question.scss
 ┃ ┃ ┗ 📜main.scss
 ┣ 📂static
 ┃ ┣ 📂fonts
 ┃ ┃ ┣ 📜lato-v20-latin-ext_latin-300.woff
 ┃ ┃ ┣ 📜lato-v20-latin-ext_latin-300.woff2
 ┃ ┃ ┣ 📜lato-v20-latin-ext_latin-300italic.woff
 ┃ ┃ ┣ 📜lato-v20-latin-ext_latin-300italic.woff2
 ┃ ┃ ┣ 📜lato-v20-latin-ext_latin-italic.woff
 ┃ ┃ ┣ 📜lato-v20-latin-ext_latin-italic.woff2
 ┃ ┃ ┣ 📜lato-v20-latin-ext_latin-regular.woff
 ┃ ┃ ┗ 📜lato-v20-latin-ext_latin-regular.woff2
 ┃ ┣ 📂images
 ┃ ┃ ┣ 📜login.svg
 ┃ ┃ ┣ 📜logo.svg
 ┃ ┃ ┣ 📜mark.svg
 ┃ ┃ ┣ 📜online-test.svg
 ┃ ┃ ┣ 📜profile.svg
 ┃ ┃ ┣ 📜register.svg
 ┃ ┃ ┣ 📜search.svg
 ┃ ┃ ┣ 📜siriuswebheader.png
 ┃ ┃ ┣ 📜stars.webp
 ┃ ┃ ┗ 📜twinkling.webp
 ┃ ┣ 📂js
 ┃ ┃ ┣ 📜darkmode.js
 ┃ ┃ ┣ 📜login-register.js
 ┃ ┃ ┣ 📜markdown-it.min.js
 ┃ ┃ ┣ 📜mathjax-config.js
 ┃ ┃ ┣ 📜navbar_submenu.js
 ┃ ┃ ┣ 📜notifications.js
 ┃ ┃ ┣ 📜pageloadanim.js
 ┃ ┃ ┣ 📜purify.min.js
 ┃ ┃ ┣ 📜purify.min.js.map
 ┃ ┃ ┣ 📜search.js
 ┃ ┃ ┣ 📜search_through_course.js
 ┃ ┃ ┣ 📜stoppageloadanim.js
 ┃ ┃ ┣ 📜tag_input.js
 ┃ ┃ ┗ 📜views.js
 ┃ ┣ 📜App.css
 ┃ ┣ 📜app.js
 ┃ ┣ 📜BreadCrumbs.css
 ┃ ┣ 📜BreadCrumbs.js
 ┃ ┣ 📜CourseCreate.js
 ┃ ┣ 📜CourseForm.vue_vue_type_script_setup_true_lang.js
 ┃ ┣ 📜CourseIndex.js
 ┃ ┣ 📜CourseIndex2.js
 ┃ ┣ 📜CourseLevelShow.js
 ┃ ┣ 📜CourseListItem.vue_vue_type_script_setup_true_lang.js
 ┃ ┣ 📜CourseShow.js
 ┃ ┣ 📜CourseShow2.js
 ┃ ┣ 📜DashboardLayout.css
 ┃ ┣ 📜DashboardLayout.js
 ┃ ┣ 📜fuzzysort.js
 ┃ ┣ 📜index.js
 ┃ ┣ 📜IndexView.css
 ┃ ┣ 📜IndexView.js
 ┃ ┣ 📜LevelShow.js
 ┃ ┣ 📜LoginView.css
 ┃ ┣ 📜LoginView.js
 ┃ ┣ 📜manifest.json
 ┃ ┣ 📜MarkdownEditor.css
 ┃ ┣ 📜MarkdownEditor.js
 ┃ ┣ 📜ProfileEdit.js
 ┃ ┣ 📜ProfileView.js
 ┃ ┣ 📜purify.es.js
 ┃ ┣ 📜QuestionCreate.js
 ┃ ┣ 📜QuestionEditCreate.css
 ┃ ┣ 📜QuestionEditCreate.js
 ┃ ┣ 📜QuestionForm.vue_vue_type_script_setup_true_lang.js
 ┃ ┣ 📜QuestionIndex.js
 ┃ ┣ 📜QuestionListItem.css
 ┃ ┣ 📜QuestionListItem.js
 ┃ ┣ 📜QuestionShow.css
 ┃ ┣ 📜QuestionShow.js
 ┃ ┣ 📜QuestionShow2.js
 ┃ ┣ 📜relativeTime.css
 ┃ ┣ 📜relativeTime.js
 ┃ ┣ 📜stars.css
 ┃ ┣ 📜UserCreate.js
 ┃ ┣ 📜UserForm.vue_vue_type_script_setup_true_lang.js
 ┃ ┣ 📜UserIndex.js
 ┃ ┣ 📜UserShow.js
 ┃ ┣ 📜userValidation.js
 ┃ ┗ 📜_commonjsHelpers.js
 ┣ 📂templates
 ┃ ┣ 📂components
 ┃ ┃ ┗ 📜markdown_editor.html
 ┃ ┣ 📂dashboard
 ┃ ┃ ┗ 📜index.html
 ┃ ┣ 📂errors
 ┃ ┃ ┣ 📜400.html
 ┃ ┃ ┣ 📜404.html
 ┃ ┃ ┗ 📜500.html
 ┃ ┣ 📂layouts
 ┃ ┃ ┗ 📜base.html
 ┃ ┣ 📂main
 ┃ ┃ ┣ 📜add_question.html
 ┃ ┃ ┣ 📜add_question_succes.html
 ┃ ┃ ┣ 📜all_courses.html
 ┃ ┃ ┣ 📜course.html
 ┃ ┃ ┣ 📜documentation.html
 ┃ ┃ ┣ 📜index.html
 ┃ ┃ ┣ 📜index_old.html
 ┃ ┃ ┣ 📜level.html
 ┃ ┃ ┣ 📜login_register.html
 ┃ ┃ ┣ 📜profile.html
 ┃ ┃ ┣ 📜question.html
 ┃ ┃ ┗ 📜search.html
 ┃ ┗ 📂utilities
 ┃ ┃ ┣ 📜macros.html
 ┃ ┃ ┗ 📜vite.html
 ┣ 📂views
 ┃ ┗ 📂__pycache__
 ┃ ┃ ┣ 📜add_question.cpython-38.pyc
 ┃ ┃ ┣ 📜all_courses.cpython-38.pyc
 ┃ ┃ ┣ 📜course.cpython-38.pyc
 ┃ ┃ ┣ 📜dashboard.cpython-38.pyc
 ┃ ┃ ┣ 📜documentation.cpython-38.pyc
 ┃ ┃ ┣ 📜errors.cpython-38.pyc
 ┃ ┃ ┣ 📜level.cpython-38.pyc
 ┃ ┃ ┣ 📜main.cpython-38.pyc
 ┃ ┃ ┣ 📜question.cpython-38.pyc
 ┃ ┃ ┣ 📜search.cpython-38.pyc
 ┃ ┃ ┣ 📜user.cpython-38.pyc
 ┃ ┃ ┗ 📜__init__.cpython-38.pyc
 ┣ 📂__pycache__
 ┃ ┣ 📜context_functions.cpython-38.pyc
 ┃ ┣ 📜models.cpython-38.pyc
 ┃ ┣ 📜routes.cpython-38.pyc
 ┃ ┣ 📜utilities.cpython-38.pyc
 ┃ ┗ 📜__init__.cpython-38.pyc
 ┣ 📜forms.py
 ┣ 📜site.db
 ┗ 📜__init__.py
```

## Backend

The backend is written in Python and uses the [Flask](https://flask.palletsprojects.com/en/2.0.x/) framework. The backend is responsible for handling requests from the frontend and communicating with the database.

### `__init__.py`

This file is the entry point for the backend. This is where the Flask app is created and the database is initialized. The routes are also registered in this file.

It sets up the following:

-   Loading the configuration from `config.py`
-   Authentication via [Flask Login](https://flask-login.readthedocs.io/en/latest/)
-   Database via [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)
-   csrf protection via [Flask WTF](https://flask-wtf.readthedocs.io/en/0.15.x/)
-   Context processors for global functions in templates via `nebula/helpers/global_functions.py`
-   Error handlers for 4xx and 5xx errors via `nebula/routes/web/errors.py`

### Routes

The routes are split into two categories: API and Web. The API routes are used for communicating with the database and the Web routes are used for rendering the frontend.

```
📂nebula
 ┣ 📂routes
 ┃ ┣ 📂api
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜api_route.py
 ┃ ┗ 📂web
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜web_route.py
 ┣ 📂src
```

::: tip More Information
For more information on the routes, see the [Routes](/developer/backend/routes) section.
:::

### Models

The models are used to define the database schema. The models are defined using [SQLAlchemy](https://docs.sqlalchemy.org/en/14/) and [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/).

Models are defined in the `models` directory. Each model is defined in its own file. For example, the `User` model is defined in `models/user.py`.

```
📂nebula
 ┣ 📂models
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜user.py
```

::: tip More Information
For more information on the models, see the [Models](/developer/backend/models) section.
:::

## Frontend

::: warning Migration in Progress
Nebula is currently in the process of migrating from `Flask` and `Jinja` templates to `Vite` and `Vue`.

The documentation is subject to change as the migration progresses.
:::

### `Flask` and `Jinja`

The frontend is written with templates using [Jinja](https://jinja.palletsprojects.com/en/3.0.x/). The frontend is responsible for rendering the pages and handling user interactions.

The html templates are located in the `nebula/templates` directory. The `templates` directory is split into several subdirectories:

```
📂nebula
 ┣ 📂templates // [!code focus:10]
 ┃ ┣ 📂errors
 ┃ ┣ 📂layouts
 ┃ ┃ ┗ 📜base.html
 ┃ ┣ 📂main
 ┃ ┃ ┣ 📜index.html
 ┃ ┃ ┗ 📜login.html
 ┃ ┗ 📂utilities
 ┃ ┃ ┣ 📜macros.html
 ┃ ┃ ┗ 📜vite.html
```

#### Layouts

The `layouts` directory contains the base template for the frontend. Individual pages can extend the base template to inherit the base layout. The base template is located at `nebula/templates/layouts/base.html`. To learn more about extending templates, see the [Jinja documentation](https://jinja.palletsprojects.com/en/3.0.x/templates/#template-inheritance).

#### Main

The `main` directory contains the individual pages for the frontend. The pages are usually rendered using the base template. The pages are located at `nebula/templates/main`.

#### Utilities

The `utilities` directory contains the macros and vite template. The macros are used to define reusable blocks of code. The macros are located at `nebula/templates/utilities/macros.html`.

The vite template is used to load vite assets. The vite template is located at `nebula/templates/utilities/vite.html`.

### Serving frontend assets with `Vite`

Currently `Vite` is used to build the frontend assets. `Vite` is a build tool that uses [ESM](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules) imports to bundle the frontend assets. `Vite` is similar to [Webpack](https://webpack.js.org/) but is much faster.

```
📦nebula/src
 ┣ 📂js
 ┣ 📂public
 ┃ ┣ 📂images
 ┃ ┗ 📂js
 ┣ 📂scss
```

Any assets that are imported in the frontend are located in the `nebula/src` directory.

During development, `Vite` is used to serve the frontend assets with their web server. Vite will watch for changes in the frontend assets and automatically reload the page.

During production, `Vite` is used to build the frontend assets. The frontend assets are built into the `nebula/static` directory. Vite will create a manifest file that maps the asset names to their hashed names. The manifest file is located at `nebula/static/manifest.json`.

::: tip More Information
Learn more about how assets are imported in nebula in the [Importing Assets](/developer/frontend/importing-assets) section.
:::

### `Vue`

::: warning Migration in Progress
Nebula is currently in the process of migrating from `Flask` and `Jinja` templates to `Vite` and `Vue`.

The documentation is subject to change as the migration progresses.
:::

The frontend is written with [Vue](https://vuejs.org/). Vue is a frontend framework that is used to create reactive components. The frontend is responsible for rendering the pages and handling user interactions.

The frontend is located in the `nebula/src/js` directory. The frontend is split into several subdirectories:

```
📦nebula/src/js
 ┣ 📂components
 ┣ 📂views
 ┣ 📂stores
 ┣ 📂vue-services
 ┣ 📂add_question
 ┣ 📂dashboard
 ┣ 📜router.ts
```

Since Nebula is still migrating there is no single frontend entry point. Currently these are the frontend entry points:

-   `nebula/templates/main/dashboard/index.html`
    -   Which imports `nebula/src/js/dashboard/dashboardMain.ts`
-   `nebula/templates/main/add_question.html`
    -   Which imports `nebula/src/js/add_question/add_question.ts`

These entry ts files import their respective Vue apps and mount them to the DOM.

#### Components

The `components` directory contains the individual components for the frontend. The components are located at `nebula/src/js/components`.

#### Views

The `views` directory contains the individual views for the frontend. The views are located at `nebula/src/js/views`.

#### Stores

Stores are used to store the state of the frontend. The stores are located at `nebula/src/js/stores`.

The stores directory contains a storeFactory.ts file. The storeFactory.ts file is used to create most of the stores. The storeFactory.ts file is located at `nebula/src/js/stores/factory/storeFactory.ts`.

#### Vue Services

Vue services are used to define reusable functions for the frontend. The vue services are located at `nebula/src/js/vue-services`.

#### `router.ts`

The `router.ts` file is used to define the routes for the frontend. The routes are located at `nebula/src/js/router.ts`.
