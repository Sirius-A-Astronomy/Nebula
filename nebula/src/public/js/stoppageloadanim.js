document.querySelectorAll(".loader").forEach((loader) => {
	setTimeout(() => {
		loader.classList.add("fade-out");
		setTimeout(() => {
			loader.remove();
		}, 200);
	}, 200);
});
