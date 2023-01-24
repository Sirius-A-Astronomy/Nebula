<script setup lang="ts">
import { ref, onMounted } from "vue";

import InfoIcon from "@components/icons/InfoIcon.vue";

// Have cookies been accepted?
const cookiesAccepted = ref(false);
const noticeVisible = ref(false);
const showPurposeModal = ref(false);

const acceptCookies = () => {
  localStorage.setItem("cookiesAccepted", "true");
  cookiesAccepted.value = true;
  noticeVisible.value = false;
  showPurposeModal.value = false;
};

const viewPurposes = () => {
  showPurposeModal.value = true;
  noticeVisible.value = false;
};

onMounted(() => {
  noticeVisible.value = localStorage.getItem("cookiesAccepted") === null;
});

const cookiePurposes: {
  name: string;
  description: string;
  items: { name: string; description: string; help?: string }[];
}[] = [
  {
    name: "Functional cookies",
    description:
      "Functional cookies are used to make the website work properly. You can set your browser to block these cookies, but some parts of the website may not work properly.",
    items: [
      {
        name: "Session",
        description:
          "Used to keep track of your session on the website. Used to keep you logged in, .",
        help: "A session cookie is a randomly generated ID that is temporarily stored in your browser until you close it. It is used so that the server can know that your requests are coming from the same browser. It is not used to identify you personally, and does not contain any personal information.",
      },
    ],
  },
  {
    name: "Local storage",
    description:
      "Used to store data locally on your device. Is not sent to the server.",
    items: [
      {
        name: "Cookies accepted",
        description:
          "Used to keep track of whether you have accepted cookies or not.",
      },

      {
        name: "Theme",
        description: "Used to keep track of your theme preference.",
      },
    ],
  },
];
</script>

<template>
  <template v-if="noticeVisible">
    <div class="cookie-notice">
      <div class="cookie-notice__content">
        <p>
          Nebula uses cookies to ensure you get the best experience on our
          website.
        </p>
      </div>

      <div class="cookie-notice__actions">
        <button class="btn btn--secondary" @click="viewPurposes">
          View purposes
        </button>

        <button class="btn btn--primary" @click="acceptCookies">Accept</button>
      </div>
    </div>
  </template>

  <template v-if="showPurposeModal">
    <div class="cookie-purposes-backdrop"></div>
    <div class="cookie-purposes">
      <div class="cookie-purposes__content">
        <button
          class="close-button"
          @click="
            () => {
              showPurposeModal = false;
              noticeVisible = true;
            }
          "
        >
          Close
        </button>
        <h2>Cookie purposes</h2>
        <p>
          Nebula uses cookies to ensure you get the best experience on our
          website.
        </p>

        <ul>
          <li v-for="purpose in cookiePurposes" :key="purpose.name">
            <h3>{{ purpose.name }}</h3>
            <p>{{ purpose.description }}</p>

            <ul>
              <li v-for="item in purpose.items" :key="item.name">
                <div class="purpose__header">
                  <h4>{{ item.name }}</h4>
                  <InfoIcon
                    v-if="item.help"
                    class="info-icon"
                    width="16"
                    height="16"
                  />
                </div>
                <div class="purpose__info" v-if="item.help">
                  {{ item.help }}
                </div>
                <p>{{ item.description }}</p>
              </li>
            </ul>
          </li>
        </ul>
      </div>

      <div class="cookie-purposes__actions">
        <button class="btn btn--primary" @click="acceptCookies">Accept</button>
      </div>
    </div>
  </template>
</template>

<style lang="scss" scoped>
.cookie-notice {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: var(--color-background-secondary, #fff);
  color: var(--color-text-primary, #000);
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  z-index: 1000;

  &__content {
    flex: 1 0;
    text-align: center;
  }

  &__actions {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    flex: 0 0;
    justify-content: center;

    .btn {
      padding: 0.5rem 1rem;
    }

    .btn--secondary {
      background-color: var(--color-background-tertiary, #fff);
      color: var(--color-text-primary, #000);
    }

    .btn--primary {
      background-color: var(--color-primary-active, #000);
      color: var(--color-background, #fff);
    }
  }
}

@media screen and (min-width: 768px) {
  .cookie-notice {
    flex-direction: row;
    align-items: center;
    padding: 1rem 2rem;
    justify-content: end;
    gap: 2rem;

    &__content {
      text-align: end;
      flex: auto;
    }

    &__actions {
      flex-wrap: nowrap;
    }
  }
}

.cookie-purposes-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

.cookie-purposes {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--color-background-secondary, #fff);
  color: var(--color-text-primary, #000);
  padding: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  margin-inline: auto;
  margin-block: auto;
  max-width: 600px;
  max-height: min(100vh, 600px);

  &__content {
    flex: 1;
    font-size: 14px;
    padding: 0.5rem;
    overflow-y: auto;

    h2 {
      font-size: 24px;
    }

    h3 {
      font-size: 18px;
    }

    h4 {
      font-size: 16px;
      margin: 0;
    }

    li {
      margin-bottom: 1rem;

      &:last-child {
        margin-bottom: 0;
      }

      p {
        font-size: 12px;
      }
    }

    .info-icon {
      cursor: pointer;
    }

    .purpose__header {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .purpose__info {
      display: none;
      background-color: var(--color-background-tertiary, #fff);
      padding: 0.5rem;
      border-radius: 0.5rem;
    }

    &:has(.info-icon:hover, .purpose__info:hover) .purpose__info {
      display: block;
    }

    .close-button {
      position: absolute;
      top: 0;
      right: 0;
      margin-top: 0.8rem;
      margin-right: 0.5rem;
      padding: 0.2rem 0.5rem;
      background-color: transparent;
      border: none;
      cursor: pointer;

      &:hover {
        background-color: var(--color-background-tertiary, #fff);
      }
    }
  }

  &__actions {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;

    .btn {
      padding: 0.5rem 1rem;
    }

    .btn--secondary {
      background-color: var(--color-background-tertiary, #fff);
      color: var(--color-text-primary, #000);
    }

    .btn--primary {
      background-color: var(--color-primary-active, #000);
      color: var(--color-background, #fff);
    }
  }
}
</style>
