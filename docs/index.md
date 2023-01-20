---
layout: home

hero:
    name: Nebula
    text: Prepare for your exams with Nebula
    tagline: Brought to you by the Kapteyn Learning Committee and Sirius A
    image:
        src: /assets/logo.svg
        alt: Nebula logo
    actions:
        - text: Get started
          theme: brand
          link: /user/getting-started
        - text: View on Gitlab
          theme: alt
          link: https://gitlab.astro.rug.nl/sirius-a/nebula

features:
    -   title: For students
        details: Learn how to use Nebula as a student. Learn how to create and format questions, answers and comments.
        link: /user/getting-started
    -   title: For Nebula moderators
        details: Learn how to use Nebula as a moderator. Learn how to moderate questions, answers and comments. Learn how to managage users, courses and questions.
        link: /moderator/getting-started
    -   title: For Nebula developers
        details: Learn how to use Nebula as a developer. Learn the project structure, how to set up a development environment and how to contribute to the project.
        link: /developer/getting-started
---


<script setup lang="ts">
    /* 
        Workaround for vitepress not going to the correct path when
        doing a full page load on a subpath.
    */

    import { useRouter, useRoute } from 'vitepress'
    import { onBeforeMount } from 'vue'

    const router = useRouter()

    onBeforeMount(() => {
        const pathParams = new URLSearchParams(window.location.search)
        const path = pathParams.get('path')
        const hash = window.location.hash

        if (path) {
            router.go("/docs/" + path + hash)
        }
    })


</script>