//testing nav and index page

describe("index", () => {
    beforeEach(() => {
        cy.visit("/");
        cy.get("h2").should("contain", "Browse");
    });

    it("should have a title", () => {
        cy.title().should("contain", "Nebula");
    });

    it("should display all courseLevels", () => {
        cy.get("a").should("contain", "First Year");
        cy.get("a").should("contain", "Second Year");
        cy.get("a").should("contain", "Third Year");
        cy.get("a").should("contain", "General");
    }
    );
    it("should have navigation to a course_level from browse", () => {
        cy.get("p > a").contains("First Year").click();
        cy.url().should("include", "/course_levels/bsc-yr1");
    });

    it("should have navigation to a course_level from nav", () => {
        cy.get(".navbar-nav").contains("Courses").realHover();
        cy.get(".dropdown-menu").contains("First Year").click();
        cy.url().should("include", "/course_levels/bsc-yr1");
    });

    it("should have navigation to a course from nav", () => {
        cy.get("a").contains("Courses").realHover();
        cy.get(".dropdown-menu > li > a").contains("First Year").realHover();
        cy.get(".dropdown-submenu > li > a").contains("Calculus 1").click();
        cy.url().should("contain", "/levels/bsc-yr1/courses/WBMA003-05");
    });

    it("Should have navigation back to the main sirius a website", () => {
        cy.get("a").contains("Sirius").should("have.attr", "href", "https://sirius.astro.rug.nl/");
    });

});