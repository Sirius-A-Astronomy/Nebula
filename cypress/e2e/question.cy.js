describe("Question page", () => {
	context("on desktop", () => {
		beforeEach(() => {
			cy.viewport(1200, 800);
			cy.visit("/course/WBPH054-05/question/2");
		});
		it("should have a title", () => {
			cy.title().should("contain", "Nebula");
			cy.title().should("contain", "This is another question");
		});
		it("should have a question", () => {
			cy.get("p").should("contain", "Question in Linear Algebra");
			cy.get("h4").should("contain", "This is another question");
		});
		it("should have an answer", () => {
			cy.get("p").should("contain", "This is the answer");
		});
		it("should have comments", () => {
			cy.get("p").should("contain", "This is an awful question");
		});
		it("shoud have a read more button that shows expanded text when clicked", () => {
			cy.get(".expandable-text > a")
				.should("contain", "Read more")
				.click({ multiple: true });
			cy.get("p").should("contain", "ΦΧΨΩΪΫ");
		});
		it("should have a read less button if text is expanded that hides the text when clicked", () => {
			cy.get(".expandable-text > a")
				.should("contain", "Read more")
				.click({ multiple: true });
			cy.get(".expandable-text > a")
				.should("contain", "Read less")
				.click({ multiple: true });
			cy.get("p").should("not.contain", "ΦΧΨΩΪΫ");
		});
	});

	context("on mobile", () => {
		beforeEach(() => {
			cy.viewport("iphone-xr");
			cy.visit("/course/WBPH054-05/question/2");
			cy.get("p").should("contain", "Question in");
		});

		it("should have a title", () => {
			cy.title().should("contain", "Nebula");
			cy.title().should("contain", "This is another question");
		});
		it("should have a question", () => {
			cy.get("p").should("contain", "Question in Linear Algebra");
			cy.get("h4").should("contain", "This is another question");
		});
		it("should have an answer", () => {
			cy.get("p").should("contain", "This is the answer");
		});
		it("should have comments", () => {
			cy.get("p").should("contain", "This is an awful question");
		});
		it("shoud have a read more button that shows expanded text when clicked", () => {
			cy.get(".expandable-text > a")
				.should("contain", "Read more")
				.click({ multiple: true });
			cy.get("p").should("contain", "ΦΧΨΩΪΫ");
		});
		it("should have a read less button if text is expanded that hides the text when clicked", () => {
			cy.get(".expandable-text > a")
				.should("contain", "Read more")
				.click({ multiple: true });
			cy.get(".expandable-text > a")
				.should("contain", "Read less")
				.click({ multiple: true });
			cy.get("p").should("not.contain", "ΦΧΨΩΪΫ");
		});
	});
});
