let mathjax = window.MathJax;

class Question {
	ranking = 0;
	matchingElements = [];
	matchingTags = [];
	matchedStringArray;
	searchResult;

	constructor(questionJSON) {
		this.id = questionJSON.id;
		this.title = DOMPurify.sanitize(questionJSON.title, {
			ALLOWED_TAGS: [],
		});
		this.content = DOMPurify.sanitize(questionJSON.content, {
			ALLOWED_TAGS: [],
		});
		this.created_at = DOMPurify.sanitize(questionJSON.created_at, {
			ALLOWED_TAGS: [],
		});
		this.url = questionJSON.url;
		this.user = questionJSON.user;
		this.user.username = DOMPurify.sanitize(this.user.username, {
			ALLOWED_TAGS: [],
		});
		this.answersCount = questionJSON.answers_count;
		this.commentsCount = questionJSON.comments_count;
		this.subjectTags = questionJSON.subject_tags;
		this.course = questionJSON.course;
		this.subject_tags_names = DOMPurify.sanitize(
			questionJSON.subject_tags_names,
			{
				ALLOWED_TAGS: [],
			}
		);
	}

	get element() {
		let questionElement = document.createElement("a");
		questionElement.classList.add("question-list-item");
		questionElement.href = this.url;

		// HEADER
		let questionListItem__Header = document.createElement("div");
		questionListItem__Header.classList.add("question-list-item__header");

		//      USERNAME
		let questionListItem__Header__UserName = document.createElement("div");
		questionListItem__Header__UserName.classList.add(
			"question-list-item__header__username"
		);
		let questionListItem__Header__UserName__Link =
			document.createElement("a");
		questionListItem__Header__UserName__Link.href = this.user.url;
		let usernameHighlighted = this.searchResult[3]
			? DOMPurify.sanitize(
					fuzzysort.highlight(
						this.searchResult[3],
						"<span>",
						"</span>"
					),
					{ ALLOWED_TAGS: ["span"] }
			  )
			: this.user.username;
		questionListItem__Header__UserName__Link.innerHTML =
			usernameHighlighted;

		questionListItem__Header__UserName.appendChild(
			questionListItem__Header__UserName__Link
		);
		//      SUBJECT_TAGS
		let questionListItem__Header__SubjectTags =
			document.createElement("div");
		questionListItem__Header__SubjectTags.classList.add(
			"question-list-item__header__subject-tags"
		);

		let subjectTagsHighlighted = (
			this.searchResult[2]
				? DOMPurify.sanitize(
						fuzzysort.highlight(
							this.searchResult[2],
							"<span>",
							"</span>"
						),
						{ ALLOWED_TAGS: ["span"] }
				  )
				: this.subject_tags_names
		).split(" ; ");

		for (let [i, subjectTag] of this.subjectTags.entries()) {
			let questionListItem__Header__SubjectTags__Tag =
				document.createElement("a");
			questionListItem__Header__SubjectTags__Tag.href = subjectTag.url;
			questionListItem__Header__SubjectTags__Tag.innerHTML =
				subjectTagsHighlighted[i];
			questionListItem__Header__SubjectTags__Tag.classList.add(
				"subject-tag"
			);
			questionListItem__Header__SubjectTags__Tag.title =
				subjectTagsHighlighted[i];
			questionListItem__Header__SubjectTags.appendChild(
				questionListItem__Header__SubjectTags__Tag
			);
		}

		//     COURSE
		let questionListItem__Header__Course = document.createElement("div");
		questionListItem__Header__Course.classList.add(
			"question-list-item__header__course"
		);
		let questionListItem__Header__Course__Link =
			document.createElement("a");
		questionListItem__Header__Course__Link.href = this.course.url;
		questionListItem__Header__Course__Link.textContent = this.course.name;
		questionListItem__Header__Course.appendChild(
			questionListItem__Header__Course__Link
		);

		questionListItem__Header.append(
			questionListItem__Header__UserName,
			questionListItem__Header__SubjectTags,
			questionListItem__Header__Course
		);

		// BODY
		let questionListItem__Body = document.createElement("div");
		questionListItem__Body.classList.add("question-list-item__body");

		//      TITLE
		let questionListItem__Body__Title = document.createElement("div");
		questionListItem__Body__Title.classList.add(
			"question-list-item__body__title"
		);
		let questionListItem__Body__Title__Link = document.createElement("a");
		questionListItem__Body__Title__Link.href = this.url;
		questionListItem__Body__Title__Link.classList.add("latex-view");

		let titleHighlighted = this.searchResult[0]
			? DOMPurify.sanitize(
					fuzzysort.highlight(
						this.searchResult[0],
						"<span>",
						"</span>"
					),
					{ ALLOWED_TAGS: ["span"] }
			  )
			: this.title;

		questionListItem__Body__Title__Link.innerHTML = titleHighlighted;
		mathjax.typesetPromise([questionListItem__Body__Title__Link]);

		questionListItem__Body__Title.appendChild(
			questionListItem__Body__Title__Link
		);

		//      CONTENT
		let questionListItem__Body__Content = document.createElement("div");
		questionListItem__Body__Content.classList.add(
			"question-list-item__body__content"
		);

		if (this.searchResult[1] && this.searchResult[1].score > -20000) {
			let contentHighlighted = DOMPurify.sanitize(
				"In content: " +
					fuzzysort.highlight(
						this.searchResult[1],
						"<span>",
						"</span>"
					),
				{ ALLOWED_TAGS: ["span"] }
			);

			questionListItem__Body__Content.innerHTML = contentHighlighted;

			questionListItem__Body__Title.appendChild(
				questionListItem__Body__Content
			);
		}

		//      POSTED AT
		let questionListItem__Body__PostedAt = document.createElement("div");
		questionListItem__Body__PostedAt.classList.add(
			"question-list-item__body__posted-at"
		);
		questionListItem__Body__PostedAt.textContent = this.created_at;

		questionListItem__Body.append(
			questionListItem__Body__Title,

			questionListItem__Body__PostedAt
		);

		// FOOTER
		let questionListItem__Footer = document.createElement("div");
		questionListItem__Footer.classList.add("question-list-item__footer");

		//      ANSWERS
		let questionListItem__Footer__Answers = document.createElement("div");
		questionListItem__Footer__Answers.classList.add(
			"question-list-item__footer__item"
		);
		questionListItem__Footer__Answers.textContent = `
                    ${this.answersCount} ${
			this.answersCount == 1 ? "answer" : "answers"
		}`;

		//      COMMENTS
		let questionListItem__Footer__Comments = document.createElement("div");
		questionListItem__Footer__Comments.classList.add(
			"question-list-item__footer__item"
		);
		questionListItem__Footer__Comments.textContent = `${
			this.commentsCount
		} ${this.commentsCount == 1 ? "comment" : "comments"}`;

		questionListItem__Footer.append(
			questionListItem__Footer__Answers,
			questionListItem__Footer__Comments
		);

		// APPEND ALL TO QUESTION ELEMENT

		questionElement.append(
			questionListItem__Header,
			questionListItem__Body,
			questionListItem__Footer
		);
		return questionElement;
	}
}
const searchInputField = document.getElementById("course-search-input-field");
const questionListContainer = document.getElementById(
	"question-list-container"
);
const questionAmount = document.getElementById("course-question-amount");
let questionsJSON = null;
let questions = [];
let awaitingServerResponse = false;

async function getCourseQuestions() {
	if (questionsJSON != null) {
		return questionsJSON;
	}
	let courseCode = searchInputField.dataset.course;

	questionsJSON = await fetch(
		"/api/get_course_questions?course_code=" + courseCode
	)
		.then((response) => response.json())
		.then((data) => {
			return data;
		})
		.catch((error) => {
			console.error("Error:", error);
		});

	return questionsJSON;
}

async function initSearch() {
	let url_string = window.location.href;
	let url = new URL(url_string);
	let query = url.searchParams.get("query");
	if (query != null) {
		searchInputField.value = query;
	}
	search();

	searchInputField.addEventListener("input", search);
}

initSearch();

async function search() {
	if (questions.length == 0 && !awaitingServerResponse) {
		awaitingServerResponse = true;
		questionsJSON = await getCourseQuestions();
		questions = [];
		for (let question of questionsJSON.questions) {
			questions.push(new Question(question));
		}
	}

	let searchInput = searchInputField.value;
	if (searchInput.length == 0) {
		questionListContainer.innerHTML = "";
		questionAmount.textContent = `${questions.length} Questions`;
		for (let question of questions) {
			question.ranking = 0;
			question.matchedStringArray = [];
			question.searchResult = [];
			questionListContainer.prepend(question.element);
		}
		return;
	}

	let searchResults = fuzzysort.go(searchInput, questions, {
		keys: ["title", "content", "subject_tags_names", "user.username"],
		scoreFn: (a) => {
			return Math.max(
				a[0] ? a[0].score : -Infinity,
				a[1] ? a[1].score : -Infinity,
				a[2] ? a[2].score : -Infinity,
				a[3] ? a[3].score - 200 : -Infinity
			);
		},
		threshold: -40000,
	});
	console.log("searchResults", searchResults);

	questionListContainer.innerHTML = "";
	for (let searchResult of searchResults) {
		let question = searchResult.obj;
		// question.ranking = searchResult.score;
		// question.matchedStringArray = [
		// 	searchResult[0] ? fuzzysort.highlight(searchResult[0]) : null,
		// 	searchResult[1] ? fuzzysort.highlight(searchResult[1]) : null,
		// 	searchResult[2] ? fuzzysort.highlight(searchResult[2]) : null,
		// 	searchResult[3] ? fuzzysort.highlight(searchResult[3]) : null,
		// ];
		question.searchResult = searchResult;
		let questionElement = question.element;
		questionListContainer.appendChild(questionElement);
	}
	questionAmount.textContent = `Showing ${searchResults.length}/${questions.length} Questions`;
}
