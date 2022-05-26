class Question {
	ranking = 0;
	matchingElements = [];
	matchingTags = [];
	_element = null;

	constructor(questionJSON) {
		this.id = questionJSON.id;
		this.title = questionJSON.title;
		this.content = questionJSON.content;
		this.created_at = questionJSON.created_at;
		this.url = questionJSON.url;
		this.user = questionJSON.user;
		this.answersCount = questionJSON.answers_count;
		this.commentsCount = questionJSON.comments_count;
		this.subjectTags = questionJSON.subject_tags;
		this.course = questionJSON.course;
	}

	get element() {
		// If the element has already been created, return it
		if (this._element) {
			return this._element;
		}
		// Otherwise, create it
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
		questionListItem__Header__UserName__Link.textContent =
			this.user.username;

		questionListItem__Header__UserName.appendChild(
			questionListItem__Header__UserName__Link
		);
		//      SUBJECT_TAGS
		let questionListItem__Header__SubjectTags =
			document.createElement("div");
		questionListItem__Header__SubjectTags.classList.add(
			"question-list-item__header__subject-tags"
		);
		for (let subjectTag of this.subjectTags) {
			let questionListItem__Header__SubjectTags__Tag =
				document.createElement("a");
			questionListItem__Header__SubjectTags__Tag.href = subjectTag.url;
			questionListItem__Header__SubjectTags__Tag.textContent =
				subjectTag.name;
			questionListItem__Header__SubjectTags__Tag.classList.add(
				"subject-tag"
			);
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
		questionListItem__Body__Title__Link.textContent = this.title;
		questionListItem__Body__Title.appendChild(
			questionListItem__Body__Title__Link
		);

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

		// Add the element to the cache
		this._element = questionElement;
		return this._element;
	}
}

let questionsJSON;

async function getQuestions() {
	if (questionsJSON != null) {
		return questionsJSON;
	}
	questionsJSON = await fetch("/api/get_questions")
		.then((response) => response.json())
		.then((data) => {
			console.log("Success:", data);
			return data;
		})
		.catch((error) => {
			console.error("Error:", error);
		});

	return questionsJSON;
}

let questions = [];
const questionListContainer = document.getElementById(
	"question-list-container"
);
const searchInputField = document.getElementById("search-input-field");

async function initSearch() {
	let url_string = window.location.href;
	let url = new URL(url_string);
	let query = url.searchParams.get("query");
	if (query != null) {
		query = query.toLowerCase();
		searchInputField.value = query;
	}
	searchInputField.addEventListener("input", search);
	search();
}

async function search() {
	questionListContainer.textContent = "";

	if (questions.length == 0) {
		questionsJSON = await getQuestions();
		for (let question of questionsJSON.questions) {
			questions.push(new Question(question));
		}
	}

	let searchInput = searchInputField.value.toLowerCase();
	if (searchInput.length == 0) {
		return;
	}

	let matchingQuestions = [];

	for (let question of questions) {
		question.ranking = 0;
		question.matchingElements = [];
		question.matchingTags = [];
		if (question.title.toLowerCase().includes(searchInput)) {
			question.ranking += 5;
			question.matchingElements.push("title");
		}
		if (question.course.name.toLowerCase().includes(searchInput)) {
			question.ranking += 1;
			question.matchingElements.push("course");
		}
		if (question.user.username.toLowerCase().includes(searchInput)) {
			question.matchingElements.push("user");
		}
		if (question.subjectTags.length > 0) {
			for (let subjectTag of question.subjectTags) {
				// if the tag matches the search input exactly, increase the ranking by a lot
				if (subjectTag.name.toLowerCase() == searchInput) {
					question.ranking += 5;
					question.matchingElements.push("subjectTag");
				}
				// if the tag contains the search input, increase the ranking by a little
				else if (subjectTag.name.toLowerCase().includes(searchInput)) {
					question.ranking += 2;
					question.matchingElements.push("subjectTag");
					question.matchingTags.push(subjectTag.name);
				}
			}
		}
		if (question.content.toLowerCase().includes(searchInput)) {
			question.ranking += 2;
			question.matchingElements.push("content");
		}

		if (question.matchingElements.length > 0) {
			matchingQuestions.push(question);
		}
	}

	matchingQuestions.sort((a, b) => {
		return b.ranking - a.ranking;
	});

	for (let question of matchingQuestions) {
		questionListContainer.appendChild(question.element);
	}
}

initSearch();
