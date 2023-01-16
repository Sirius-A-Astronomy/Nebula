<script setup lang="ts">
import { authenticatedUser } from "@stores/sessionStore";

import OnlineTest from "@public/images/online-test.svg";
</script>

<template>
	<main id="Main" class="no-header-margin no-footer-margin">
		<div class="container-background">
			<div class="stars"></div>
			<div class="twinkling"></div>
			<div class="container-index">
				<div class="panel left-panel">
					<section class="container-introduction">
						<div class="content">
							{% if current_user.is_anonymous %}
							<h2>Welcome to Nebula!</h2>
							{% else %}
							<h2>
								Welcome back to Nebula,
								{{ authenticatedUser.first_name }}!
							</h2>
							{% endif %}
							<p>
								This is the Nebula Database by the Kapteyn
								Learning Community.
							</p>
							<p>
								It is a repository of user-submitted practice
								questions.
							</p>
						</div>

						<div class="image">
							<img :src="OnlineTest" alt="" />
						</div>
					</section>
				</div>
				<div class="panel right-panel">
					<section class="container-index-browse">
						<h2>Browse the Nebula</h2>
						<p>
							<a
								class="button-accent on-dark"
								href="{{ url_for('web.courses.all_courses')}}"
								>All Courses</a
							>
						</p>
						<h3>Bachelor</h3>
						{% for course_level in bsc_levels %}
						level_list_item(course_level) {% endfor %}
						<h3>Master</h3>
						{% for course_level in msc_levels %}
						level_list_item(course_level) {% endfor %}
					</section>
					<section class="container-add-question">
						<h2>Want to learn how to use nebula?</h2>
						<a class="btn btn-primary" href="#"
							>Go to documentation</a
						>
					</section>
				</div>
			</div>
		</div>
	</main>
</template>

<style lang="scss" scoped></style>
