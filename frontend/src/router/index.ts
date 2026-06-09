import { createRouter, createWebHistory } from 'vue-router'
import HomepageIndex from "@/views/homepage/HomepageIndex.vue";
import FriendIndex from "@/views/friend/FriendIndex.vue";
import CreateIndex from "@/views/create/CreateIndex.vue";
import NotFoundIndex from "@/views/error/NotFoundIndex.vue";
import LoginIndex from "@/views/user/account/LoginIndex.vue";
import RegisterIndex from "@/views/user/account/RegisterIndex.vue";
import SpaceIndex from "@/views/user/space/SpaceIndex.vue";
import ProfileIndex from "@/views/user/profile/ProfileIndex.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: HomepageIndex,
      name: 'homepage',
    },
    {
      path: '/friend/',
      component: FriendIndex,
      name: 'friend',
    },
    {
      path: '/create/',
      component: CreateIndex,
      name: 'create',
    },
    {
      path: '/404/',
      component: NotFoundIndex,
      name: '404',
    },
    {
      path: '/user/account/login',
      component: LoginIndex,
      name: 'user-account-login',
    },
    {
      path: '/user/account/register',
      component: RegisterIndex,
      name: 'user-account-register',
    },
    {
      path: '/user/space/:user_id/',
      component: SpaceIndex,
      name: 'user-space',
    },
    {
      path: '/user/profile/',
      component: ProfileIndex,
      name: 'user-profile',
    },
    {
      path: '/:pathMatch(.*)*',
      component: NotFoundIndex,
      name: 'not-found',
    },
  ],
})

export default router
