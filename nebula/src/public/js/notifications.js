class Notification {
	read;
	uuid;
	constructor(element) {
		this.action = element.querySelector(
			".notifications__list__item__actions__read"
		);
		this.element = element;
		this.read = this.action.dataset.read == "true";
		this.uuid = this.action.dataset.uuid;
		this.markAsRead = this.markAsRead.bind(this);
		this.markAsUnread = this.markAsUnread.bind(this);
		this.toggleRead = this.toggleRead.bind(this);

		this.action.addEventListener("click", this.toggleRead);

		if (this.read) {
			this.action.textContent = "Mark as unread";
		} else {
			this.action.textContent = "Mark as read";
		}
	}

	async toggleRead() {
		let result = await markNotificationAsRead(this.uuid, !this.read);
		if (result.success) {
			if (result.readConfirm) {
				this.markAsRead();
			} else {
				this.markAsUnread();
			}
		} else {
			console.log("Error marking notification as read");
		}
	}

	markAsRead() {
		if (this.read == true) return;
		this.read = true;
		this.action.textContent = "Mark as unread";
		this.action.setAttribute("data-read", "true");
		this.element.classList.remove("unread");
		notificationToggle.dataset.unreadCount--;
		if (notificationToggle.dataset.unreadCount == 0) {
			notificationToggle.classList.remove("unread");
			document
				.querySelector(".notifications__list")
				.classList.remove("notifications__list--active");
		}
	}

	markAsUnread() {
		if (this.read == false) return;
		this.read = false;
		this.action.textContent = "Mark as read";
		this.action.setAttribute("data-read", "false");
		this.element.classList.add("unread");
		notificationToggle.dataset.unreadCount++;
		notificationToggle.classList.add("unread");
	}
}

let notificationToggle = document.querySelector(".notifications__toggle");

if (notificationToggle) {
	notificationToggle.addEventListener("click", function (e) {
		e.preventDefault();
		notificationToggle.classList.toggle("notifications__toggle--active");
		document
			.querySelector(".notifications__list")
			.classList.toggle("notifications__list--active");
	});
}

async function markNotificationAsRead(notificationUUID, read) {
	let success, readConfirm;
	try {
		const response = await fetch("/api/mark_notification_as_read", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": window.CSRF_TOKEN,
			},
			body: JSON.stringify({
				notification_uuid: notificationUUID,
				read: read,
			}),
		});

		const data = await response.json();
		readConfirm = data.read;
		success = data.success;
	} catch (error) {
		console.error("Error:", error);
		success = false;
	}

	return { success, readConfirm };
}

let notificationElements = document.querySelectorAll(
	".notifications__list__item"
);

let notifications = [...notificationElements].map(
	(notification) => new Notification(notification)
);

document
	.querySelectorAll(".notifications__list__header__read-all")
	.forEach((element) => {
		element.addEventListener("click", function (e) {
			e.preventDefault();
			notifications.forEach((notification) => {
				if (!notification.read) notification.toggleRead();
			});
			document
				.querySelector(".notifications__list")
				.classList.remove("notifications__list--active");
		});
	});
