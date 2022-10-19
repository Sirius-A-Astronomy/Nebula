//testing nav and index page

describe("index", () => {
    context('on desktop', () => {
        beforeEach(() => {
            cy.viewport(1200, 800)
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
            cy.url().should("include", "/bsc-yr1");
        });

        it("should have navigation to a course_level from nav", () => {
            cy.get(".navbar-nav").contains("Courses").realHover();
            cy.get(".dropdown-menu").contains("First Year").click();
            cy.url().should("include", "/bsc-yr1");
        });

        it("should have navigation to a course from nav", () => {
            cy.get("a").contains("Courses").realHover();
            cy.get(".dropdown-menu > li > a").contains("First Year").realHover();
            cy.get(".dropdown-submenu > li > a").contains("Calculus 1").click();
            cy.url().should("contain", "WBMA003-05");
        });
    });

    context('on mobile', () => {
        beforeEach(() => {
            cy.viewport('iphone-xr')
            cy.visit("/");
            cy.get("h2").should("contain", "Browse");
        });

        it('should have a title', () => {
            cy.title().should("contain", "Nebula");
        });

        it('should display all courseLevels', () => {
            cy.get("a").should("contain", "First Year");
            cy.get("a").should("contain", "Second Year");
            cy.get("a").should("contain", "Third Year");
            cy.get("a").should("contain", "General");
        });

        it('should have navigation to a course_level from browse', () => {
            cy.get("p > a").contains("First Year").click();
            cy.url().should("include", "/bsc-yr1");
        });

        it('should have navigation to a course from nav', () => {
            cy.get(".navbar-toggler").click();
            cy.get(".navbar-nav").contains("Courses").click();
            cy.get(".dropdown-menu").contains("First Year").click();
            cy.get(".dropdown-submenu").contains("Calculus 1").click();
            cy.url().should("contain", "WBMA003-05");
        });
    });
});
