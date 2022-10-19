describe("login", () => {
	context("on desktop", () => {
		beforeEach(() => {
			cy.viewport(1200, 800);
			cy.visit("/logout");
			cy.visit("/login");
			cy.get("h2").should("contain", "Login");
		});

		it("should have a title", () => {
			cy.title().should("contain", "Nebula").and("contain", "Login");
		});

		it("should have a login form", () => {
			cy.get(".sign-in-form").should("contain", "Username");
			cy.get(".sign-in-form").should("contain", "Password");
			cy.get(".sign-in-form").should("contain", "Login");
		});

		it("should be able to login", () => {
			cy.get(".sign-in-form input[name=username]").type("pieterh");
			cy.get(".sign-in-form input[name=password]").type("unsafe");
			cy.get(".sign-in-form input[name=login_submit]")
				.contains("Login")
				.click();
			cy.url().should("include", "/");
			cy.get(".content > h2").should("contain", "Welcome back");
		});

		it("should not be able to login with a wrong password and show feedback", () => {
			cy.get(".sign-in-form input[name=username]").type("pieterh");
			cy.get(".sign-in-form input[name=password]").type("wrong");
			cy.get(".sign-in-form input[name=login_submit]")
				.contains("Login")
				.click();
			cy.url().should("include", "/login");
			cy.get(".sign-in-form .input-feedback").should(
				"contain",
				"Invalid username or password"
			);
		});

		it("should not be able to login with a wrong username and show feedback", () => {
			cy.get(".sign-in-form input[name=username]").type("wrong");
			cy.get(".sign-in-form input[name=password]").type("unsafe");
			cy.get(".sign-in-form input[name=login_submit]")
				.contains("Login")
				.click();
			cy.url().should("include", "/login");
			cy.get(".sign-in-form .input-feedback").should(
				"contain",
				"Invalid username or password"
			);
		});

        it("should have a link to the register page", () => {
            cy.get("a").contains("Create an accont", {matchCase: false}).click();
            cy.url().should("include", "/register");
        }
	});
});
