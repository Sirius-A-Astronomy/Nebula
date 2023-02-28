<script setup lang="ts">
import { RouterLink } from "vue-router";
import type { Question } from "@stores/questionStore";
import SubjectTag from "@components/subjectTag/SubjectTag.vue";

import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";

dayjs.extend(relativeTime);

defineProps<{
    question: Question;
}>();
</script>

<template>
    <RouterLink
        class="question-list-item"
        :to="{
            name: 'question.show',
            params: {
                id: question.id,
            },
        }"
    >
        <div class="question-list-item__header">
            <div class="question-list-item__header__username">
                <div>
                    {{ question.user.first_name }} {{ question.user.last_name }}
                </div>
            </div>
            <div class="question-list-item__header__subject-tags">
                <SubjectTag
                    v-for="subject_tag in question.subject_tags"
                    :subject-tag="subject_tag"
                    :key="subject_tag.id"
                    >{{ subject_tag.name }}</SubjectTag
                >
            </div>
            <div class="question-list-item__header__course">
                <RouterLink
                    :to="{
                        name: 'course.show',
                        params: {
                            id: question.course.id,
                        },
                    }"
                    >{{ question.course.name }}</RouterLink
                >
            </div>
        </div>

        <div class="question-list-item__body">
            <div class="question-list-item__body__title">
                <a
                    href="{{ url_for('web.question.question', question_uuid=question.uuid, course_code=question.course.code, course_level_code=question.course.course_level.code) }}"
                    class="question-list-item__body__title__link latex-view"
                >
                    {{ question.title }}
                </a>
            </div>

            <div class="question-list-item__body__posted-at">
                {{ dayjs(question.meta.created_at).fromNow() }}
            </div>
        </div>

        <div class="question-list-item__footer">
            <div class="question-list-item__footer__item">
                {{ question.answers?.length }}
                {{ question.answers?.length == 1 ? "Answer" : "Answers" }}
            </div>
            <div class="question-list-item__footer__item">
                {{ question.comments?.length }}
                {{ question.comments?.length == 1 ? "Comment" : "Comments" }}
            </div>
        </div>
    </RouterLink>
</template>

<style lang="scss" scoped>
.question-list-item {
    background-color: transparent;
    display: block;
    padding-bottom: 1rem;
    color: var(--color-text-primary);
    cursor: pointer;

    &:hover {
        color: var(--color-text-primary);
    }

    &:focus-within {
        background-color: var(--color-background-secondary);
    }

    &__header {
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        flex-wrap: wrap;
        margin-bottom: 0.2rem;
        gap: 0.5rem;

        &__username {
            margin-right: auto;

            a {
                font-weight: 400;
                letter-spacing: 0.095em;
                font-size: 1rem;
                color: var(--color-text-primary);
            }

            span {
                font-weight: 700;
                text-decoration: underline;
                text-decoration-color: var(--color-primary-active);
            }
        }

        &__subject-tags {
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: flex-end;
            gap: 0.5rem;

            // span {
            //     font-weight: 700;
            // }
        }

        // subject-tag is styled in _tags.scss
        &__course {
            a {
                font-weight: 300;
                font-size: 0.875rem;
                letter-spacing: 0.095em;
                color: var(--color-text-primary);
            }
            span {
                font-weight: 700;
                text-decoration: underline;
                text-decoration-color: var(--color-primary-active);
            }
        }
    }

    &__body {
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: flex-start;
        margin-bottom: 0.2rem;

        flex-wrap: wrap;

        &__title {
            margin-right: auto;
            font-style: normal;
            font-weight: 400;
            line-height: 1.075rem;
            font-size: 1rem;
            letter-spacing: 0.095em;

            flex: 1 1 auto;

            a {
                color: var(--color-primary-active);
            }

            span {
                font-weight: 700;
                text-decoration: underline;
                text-decoration-color: var(--color-primary-active);
            }
        }

        &__posted-at {
            font-style: normal;
            font-weight: 300;
            line-height: 1.075rem;
            font-size: 0.875rem;
            letter-spacing: 0.095em;

            flex: 0 0 max-content;
        }
    }

    &__footer {
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: center;
        gap: 0.875rem;

        &__item {
            font-style: normal;
            font-weight: 500;
            font-size: 0.875rem;
            line-height: 1.075rem;
            letter-spacing: 0.095em;
        }
    }
}

@media (max-width: 576px) {
    .question-list-item {
        display: grid;
        gap: 0.2rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--color-background-tertiary);
        margin-bottom: 0.5rem;

        // &,
        // & * {
        // 	outline: #aaffff33 solid 1px;
        // }

        &__footer {
            grid-column: 1 / span 3;
            grid-row: 1 / 2;
        }

        &__body {
            grid-column: 1 / span 3;
            grid-row: 2 / 3;
            margin-bottom: 0;

            &__title {
                font-size: 1.1rem;
            }

            &__content {
                font-size: 0.875rem;
            }
        }

        &__header {
            grid-column: 1 / span 3;
            grid-row: 3 / 4;
            display: flex;
            gap: 0.2rem;

            &__username {
                order: 1;
            }

            &__course {
                order: 2;
            }

            &__subject-tags {
                order: 3;
                flex-basis: 100%;
                justify-content: flex-start;
            }
        }
    }
}
</style>
