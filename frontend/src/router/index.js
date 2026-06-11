import { createRouter, createWebHistory } from 'vue-router'
import HomepageIndex from "@/views/homepage/HomepageIndex.vue";
import FriendIndex from "@/views/friend/FriendIndex.vue";
import CreateIndex from "@/views/create/CreateIndex.vue";
import NotFoundIndex from "@/views/error/NotFoundIndex.vue";
import LoginIndex from "@/views/user/account/LoginIndex.vue";
import RegisterIndex from "@/views/user/account/RegisterIndex.vue";
import SpaceIndex from "@/views/user/space/SpaceIndex.vue";
import ProfileIndex from "@/views/user/profile/ProfileIndex.vue";
import {useUserStore} from "@/stores/user.js";
import UpdateCharacter from "@/views/create/character/UpdateCharacter.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: HomepageIndex,
      name: 'homepage',
      meta:{
        needLogin: false,
      },
    },
    {
      path: '/friend/',
      component: FriendIndex,
      name: 'friend',
      meta:{
        needLogin: true,
      },
    },
    {
      path: '/create/',
      component: CreateIndex,
      name: 'create',
      meta:{
        needLogin: true,
      },
    },
    {
      path: '/create/character/update/:character_id/',
      component: UpdateCharacter,
      name: 'update-character',
      meta: {
        needLogin: true,
      },
    },
    {
      path: '/404/',
      component: NotFoundIndex,
      name: '404',
      meta:{
        needLogin: false,
      },
    },
    {
      path: '/user/account/login',
      component: LoginIndex,
      name: 'user-account-login',
      meta:{
        needLogin: false,
      },
    },
    {
      path: '/user/account/register',
      component: RegisterIndex,
      name: 'user-account-register',
      meta:{
        needLogin: false,
      },
    },
    {
      path: '/user/space/:user_id/',
      component: SpaceIndex,
      name: 'user-space',
      meta:{
        needLogin: false,
      },
    },
    {
      path: '/user/profile/',
      component: ProfileIndex,
      name: 'user-profile',
      meta:{
        needLogin: true,
      },
    },
    {
      path: '/:pathMatch(.*)*',
      component: NotFoundIndex,
      name: 'not-found',
      meta:{
        needLogin: false,
      },
    },
  ],
})

// router.beforeEach((to, from) => {
//   const user=useUserStore()
//   if(to.meta.needLogin && !user.isLogin()){
//     return {
//       name:'user-account-login',
//     }
//   }
//   else return true
// })

router.beforeEach(async (to, from) => {
    const userStore = useUserStore();

    if (to.meta.needLogin) {
        // 如果未登录，尝试获取用户信息
        if (!userStore.isLogin()) {
            try {
                // 调用新增的 fetchUserInfo 方法
                const success = await userStore.fetchUserInfo();
                if (!success) {
                    return {
                        name: 'user-account-login',
                        query: { redirect: to.fullPath }
                    };
                }
            } catch (error) {
                return {
                    name: 'user-account-login',
                    query: { redirect: to.fullPath }
                };
            }
        }

        // 最终检查是否登录成功
        if (!userStore.isLogin()) {
            return {
                name: 'user-account-login',
                query: { redirect: to.fullPath }
            };
        }
    }

    return true;
});

export default router
