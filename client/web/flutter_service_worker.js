'use strict';
const MANIFEST = 'flutter-app-manifest';
const TEMP = 'flutter-temp-cache';
const CACHE_NAME = 'flutter-app-cache';

const RESOURCES = {"assets/AssetManifest.bin": "c24ea5c829f3f0967bcc1a1d122684ad",
"assets/AssetManifest.bin.json": "79de4d6972ff21dcbff7b81f55345111",
"assets/AssetManifest.json": "7a2d8b4c3c1e58cfe0c81ceef54ad992",
"assets/assets/captcha_img/0.png": "58b872be7cbd2ecd7c21967704db09a1",
"assets/assets/captcha_img/1.png": "4b19b88f381dda5c175e3d2e744bd044",
"assets/assets/captcha_img/10.png": "8a8897e3391ab21d86d5b52574acb3ed",
"assets/assets/captcha_img/11.png": "449d9a24adcb718915a40235a618eaa0",
"assets/assets/captcha_img/12.png": "427ec589f8c74e8f0d7304bdf3e1979a",
"assets/assets/captcha_img/13.png": "4167bc3aa829175698f9e3ea375e10ce",
"assets/assets/captcha_img/14.png": "fc0b8e8a79363d102f92893afa458d55",
"assets/assets/captcha_img/15.png": "354578d054df4af170e2238f48480158",
"assets/assets/captcha_img/16.png": "f8eeeb641fba32b77473e53ea7186bd9",
"assets/assets/captcha_img/17.png": "2fa56d0cc50b9b13360c9da64002be7a",
"assets/assets/captcha_img/18.png": "c3decee8eb3fef10e512ff80bab580cb",
"assets/assets/captcha_img/19.png": "bfd15b0af06466d0303492db6cd8d2ec",
"assets/assets/captcha_img/2.png": "808ee7753ceb615bd3a6460cd780f893",
"assets/assets/captcha_img/20.png": "660aff47e1f92c4780863462fdedfd42",
"assets/assets/captcha_img/21.png": "99f5d520ede046eac57c2c6727506f99",
"assets/assets/captcha_img/22.png": "12c294ca99d80898002f6f075de41374",
"assets/assets/captcha_img/23.png": "6b97fcb283b74484bbbf079b7cd8063b",
"assets/assets/captcha_img/24.png": "469d4055b1bd841fc971b926532f9d9b",
"assets/assets/captcha_img/3.png": "cd9759e551d1dbddce81229fd9c14ab8",
"assets/assets/captcha_img/4.png": "f734e41638f25d6480bba0e46131408e",
"assets/assets/captcha_img/5.png": "da18e483e84ea426073fde79c948003e",
"assets/assets/captcha_img/6.png": "d90786503cc1c222f8237dbe3aaf060a",
"assets/assets/captcha_img/7.png": "1fca2c37753ef21106d71c7ba3cf01b4",
"assets/assets/captcha_img/8.png": "70d077655bfac8bebb3b2b1a90c7d072",
"assets/assets/captcha_img/9.png": "13568ae0871f8fbdef89a840baed304a",
"assets/assets/dotenv": "801aa283fc0b5af7fef83384822e0d0c",
"assets/assets/fintel.png": "e43bcf9794f709795c5f0c18d12cfd23",
"assets/assets/fire.svg": "7cbacb4e0cf7560c2939be792eae9dda",
"assets/assets/github_dark_logo.svg": "8dcc6b5262f3b6138b1566b357ba89a9",
"assets/assets/github_light_logo.svg": "a0b00583d93c2f7084ad151ee0849934",
"assets/assets/google_logo.svg": "edd0e34f60d7ca4a2f4ece79cff21ae3",
"assets/assets/microsoft_logo.svg": "363fdd53d34303b727d9dab161b8e88b",
"assets/assets/sad_face.png": "ee1d6882fa19ec1ac2e632942d2fa819",
"assets/assets/skeltal.png": "feb5d855d43d2ef4bbec42bcdd931efe",
"assets/assets/skeltal_dashboard.png": "cdacd68f36a58bed7d43204112731527",
"assets/FontManifest.json": "3ddd9b2ab1c2ae162d46e3cc7b78ba88",
"assets/fonts/MaterialIcons-Regular.otf": "43e9e8a4fe3b12e4455dc091f1d62e47",
"assets/html/recaptcha.html": "db4dab1409af00d00fa935e0451edd1b",
"assets/NOTICES": "6108479ad9578ef083de7c8bc1fc62e1",
"assets/packages/font_awesome_flutter/lib/fonts/fa-brands-400.ttf": "a4c5103d5d7302504349d94f4f712b2c",
"assets/packages/font_awesome_flutter/lib/fonts/fa-regular-400.ttf": "f3307f62ddff94d2cd8b103daf8d1b0f",
"assets/packages/font_awesome_flutter/lib/fonts/fa-solid-900.ttf": "04f83c01dded195a11d21c2edf643455",
"assets/packages/supabase_auth_ui/assets/logos/google_light.png": "f243a900707589f1b21af980454090bd",
"assets/packages/supabase_auth_ui/assets/logos/kakao.png": "7e156d594910fef4ae12696161c47a2f",
"assets/packages/supabase_auth_ui/assets/logos/keycloak.png": "ea74380ccc89dbc26bd0281dd46ee942",
"assets/packages/supabase_auth_ui/assets/logos/notion.png": "6b95dbedeafea10db8a51daccd7e31a4",
"assets/packages/supabase_auth_ui/assets/logos/workOS.png": "7ddd6d5a2e3b4dc4dbb1a2ee9ab8cd5b",
"assets/shaders/ink_sparkle.frag": "ecc85a2e95f5e9f53123dcaf8cb9b6ce",
"assets/vault/vault.json": "6bf84ce11c8001a59aca4832f17c4ec6",
"canvaskit/canvaskit.js": "c86fbd9e7b17accae76e5ad116583dc4",
"canvaskit/canvaskit.js.symbols": "38cba9233b92472a36ff011dc21c2c9f",
"canvaskit/canvaskit.wasm": "3d2a2d663e8c5111ac61a46367f751ac",
"canvaskit/chromium/canvaskit.js": "43787ac5098c648979c27c13c6f804c3",
"canvaskit/chromium/canvaskit.js.symbols": "4525682ef039faeb11f24f37436dca06",
"canvaskit/chromium/canvaskit.wasm": "f5934e694f12929ed56a671617acd254",
"canvaskit/skwasm.js": "445e9e400085faead4493be2224d95aa",
"canvaskit/skwasm.js.symbols": "741d50ffba71f89345996b0aa8426af8",
"canvaskit/skwasm.wasm": "e42815763c5d05bba43f9d0337fa7d84",
"canvaskit/skwasm.worker.js": "bfb704a6c714a75da9ef320991e88b03",
"captcha_img/0.png": "58b872be7cbd2ecd7c21967704db09a1",
"captcha_img/1.png": "4b19b88f381dda5c175e3d2e744bd044",
"captcha_img/10.png": "8a8897e3391ab21d86d5b52574acb3ed",
"captcha_img/11.png": "449d9a24adcb718915a40235a618eaa0",
"captcha_img/12.png": "427ec589f8c74e8f0d7304bdf3e1979a",
"captcha_img/13.png": "4167bc3aa829175698f9e3ea375e10ce",
"captcha_img/14.png": "fc0b8e8a79363d102f92893afa458d55",
"captcha_img/15.png": "354578d054df4af170e2238f48480158",
"captcha_img/16.png": "f8eeeb641fba32b77473e53ea7186bd9",
"captcha_img/17.png": "2fa56d0cc50b9b13360c9da64002be7a",
"captcha_img/18.png": "c3decee8eb3fef10e512ff80bab580cb",
"captcha_img/19.png": "bfd15b0af06466d0303492db6cd8d2ec",
"captcha_img/2.png": "808ee7753ceb615bd3a6460cd780f893",
"captcha_img/20.png": "660aff47e1f92c4780863462fdedfd42",
"captcha_img/21.png": "99f5d520ede046eac57c2c6727506f99",
"captcha_img/22.png": "12c294ca99d80898002f6f075de41374",
"captcha_img/23.png": "6b97fcb283b74484bbbf079b7cd8063b",
"captcha_img/24.png": "469d4055b1bd841fc971b926532f9d9b",
"captcha_img/3.png": "cd9759e551d1dbddce81229fd9c14ab8",
"captcha_img/4.png": "f734e41638f25d6480bba0e46131408e",
"captcha_img/5.png": "da18e483e84ea426073fde79c948003e",
"captcha_img/6.png": "d90786503cc1c222f8237dbe3aaf060a",
"captcha_img/7.png": "1fca2c37753ef21106d71c7ba3cf01b4",
"captcha_img/8.png": "70d077655bfac8bebb3b2b1a90c7d072",
"captcha_img/9.png": "13568ae0871f8fbdef89a840baed304a",
"dotenv": "801aa283fc0b5af7fef83384822e0d0c",
"favicon.png": "c7c3d5c97140a98e5cacbe6ca00356df",
"fintel.png": "e43bcf9794f709795c5f0c18d12cfd23",
"fire.svg": "7cbacb4e0cf7560c2939be792eae9dda",
"flutter.js": "c71a09214cb6f5f8996a531350400a9a",
"github_dark_logo.png": "43ce87609eb221d09d4832a9c0e709d0",
"github_dark_logo.svg": "8dcc6b5262f3b6138b1566b357ba89a9",
"github_light_logo.png": "1dee40f2668d5c719eafa2c89296f5e7",
"github_light_logo.svg": "a0b00583d93c2f7084ad151ee0849934",
"google_logo.png": "b75aecaf9e70a9b1760497e33bcd6db1",
"google_logo.svg": "edd0e34f60d7ca4a2f4ece79cff21ae3",
"icons/Icon-192.png": "ac9a721a12bbc803b44f645561ecb1e1",
"icons/Icon-512.png": "96e752610906ba2a93c65f8abe1645f1",
"icons/Icon-maskable-192.png": "c457ef57daa1d16f64b27b786ec2ea3c",
"icons/Icon-maskable-512.png": "301a7604d45b3e739efc881eb04896ea",
"index.html": "f2be3d7bead52a93929e7af85fbda294",
"/": "f2be3d7bead52a93929e7af85fbda294",
"main-icon.png": "c1e436b1c29204d242c34a8417f01c11",
"main.dart.js": "5dd78b74b116e91cab2dc6e15cfb0688",
"manifest.json": "e158c3fe3d7ad988eb8f6e99cf2455c5",
"microsoft_logo%20copy.png": "d9ddf816aab8d5e5fdbff6d065a9cfb2",
"microsoft_logo%20copy.svg": "363fdd53d34303b727d9dab161b8e88b",
"microsoft_logo.png": "d9ddf816aab8d5e5fdbff6d065a9cfb2",
"microsoft_logo.svg": "363fdd53d34303b727d9dab161b8e88b",
"res/fintel.png": "e43bcf9794f709795c5f0c18d12cfd23",
"res/fire.svg": "7cbacb4e0cf7560c2939be792eae9dda",
"res/github_dark_logo.png": "43ce87609eb221d09d4832a9c0e709d0",
"res/github_dark_logo.svg": "8dcc6b5262f3b6138b1566b357ba89a9",
"res/github_light_logo.png": "1dee40f2668d5c719eafa2c89296f5e7",
"res/github_light_logo.svg": "a0b00583d93c2f7084ad151ee0849934",
"res/google_logo.png": "b75aecaf9e70a9b1760497e33bcd6db1",
"res/google_logo.svg": "edd0e34f60d7ca4a2f4ece79cff21ae3",
"res/sad_face.png": "ee1d6882fa19ec1ac2e632942d2fa819",
"res/skeltal.png": "feb5d855d43d2ef4bbec42bcdd931efe",
"res/skeltal_dashboard.png": "cdacd68f36a58bed7d43204112731527",
"sad_face%20copy.png": "ee1d6882fa19ec1ac2e632942d2fa819",
"sad_face.png": "ee1d6882fa19ec1ac2e632942d2fa819",
"skeltal%20copy.png": "feb5d855d43d2ef4bbec42bcdd931efe",
"skeltal.png": "feb5d855d43d2ef4bbec42bcdd931efe",
"skeltal_dashboard%20copy.png": "cdacd68f36a58bed7d43204112731527",
"skeltal_dashboard.png": "cdacd68f36a58bed7d43204112731527",
"version.json": "8c125d67e652978c457c4c349e2acda8"};
// The application shell files that are downloaded before a service worker can
// start.
const CORE = ["main.dart.js",
"index.html",
"assets/AssetManifest.bin.json",
"assets/FontManifest.json"];

// During install, the TEMP cache is populated with the application shell files.
self.addEventListener("install", (event) => {
  self.skipWaiting();
  return event.waitUntil(
    caches.open(TEMP).then((cache) => {
      return cache.addAll(
        CORE.map((value) => new Request(value, {'cache': 'reload'})));
    })
  );
});
// During activate, the cache is populated with the temp files downloaded in
// install. If this service worker is upgrading from one with a saved
// MANIFEST, then use this to retain unchanged resource files.
self.addEventListener("activate", function(event) {
  return event.waitUntil(async function() {
    try {
      var contentCache = await caches.open(CACHE_NAME);
      var tempCache = await caches.open(TEMP);
      var manifestCache = await caches.open(MANIFEST);
      var manifest = await manifestCache.match('manifest');
      // When there is no prior manifest, clear the entire cache.
      if (!manifest) {
        await caches.delete(CACHE_NAME);
        contentCache = await caches.open(CACHE_NAME);
        for (var request of await tempCache.keys()) {
          var response = await tempCache.match(request);
          await contentCache.put(request, response);
        }
        await caches.delete(TEMP);
        // Save the manifest to make future upgrades efficient.
        await manifestCache.put('manifest', new Response(JSON.stringify(RESOURCES)));
        // Claim client to enable caching on first launch
        self.clients.claim();
        return;
      }
      var oldManifest = await manifest.json();
      var origin = self.location.origin;
      for (var request of await contentCache.keys()) {
        var key = request.url.substring(origin.length + 1);
        if (key == "") {
          key = "/";
        }
        // If a resource from the old manifest is not in the new cache, or if
        // the MD5 sum has changed, delete it. Otherwise the resource is left
        // in the cache and can be reused by the new service worker.
        if (!RESOURCES[key] || RESOURCES[key] != oldManifest[key]) {
          await contentCache.delete(request);
        }
      }
      // Populate the cache with the app shell TEMP files, potentially overwriting
      // cache files preserved above.
      for (var request of await tempCache.keys()) {
        var response = await tempCache.match(request);
        await contentCache.put(request, response);
      }
      await caches.delete(TEMP);
      // Save the manifest to make future upgrades efficient.
      await manifestCache.put('manifest', new Response(JSON.stringify(RESOURCES)));
      // Claim client to enable caching on first launch
      self.clients.claim();
      return;
    } catch (err) {
      // On an unhandled exception the state of the cache cannot be guaranteed.
      console.error('Failed to upgrade service worker: ' + err);
      await caches.delete(CACHE_NAME);
      await caches.delete(TEMP);
      await caches.delete(MANIFEST);
    }
  }());
});
// The fetch handler redirects requests for RESOURCE files to the service
// worker cache.
self.addEventListener("fetch", (event) => {
  if (event.request.method !== 'GET') {
    return;
  }
  var origin = self.location.origin;
  var key = event.request.url.substring(origin.length + 1);
  // Redirect URLs to the index.html
  if (key.indexOf('?v=') != -1) {
    key = key.split('?v=')[0];
  }
  if (event.request.url == origin || event.request.url.startsWith(origin + '/#') || key == '') {
    key = '/';
  }
  // If the URL is not the RESOURCE list then return to signal that the
  // browser should take over.
  if (!RESOURCES[key]) {
    return;
  }
  // If the URL is the index.html, perform an online-first request.
  if (key == '/') {
    return onlineFirst(event);
  }
  event.respondWith(caches.open(CACHE_NAME)
    .then((cache) =>  {
      return cache.match(event.request).then((response) => {
        // Either respond with the cached resource, or perform a fetch and
        // lazily populate the cache only if the resource was successfully fetched.
        return response || fetch(event.request).then((response) => {
          if (response && Boolean(response.ok)) {
            cache.put(event.request, response.clone());
          }
          return response;
        });
      })
    })
  );
});
self.addEventListener('message', (event) => {
  // SkipWaiting can be used to immediately activate a waiting service worker.
  // This will also require a page refresh triggered by the main worker.
  if (event.data === 'skipWaiting') {
    self.skipWaiting();
    return;
  }
  if (event.data === 'downloadOffline') {
    downloadOffline();
    return;
  }
});
// Download offline will check the RESOURCES for all files not in the cache
// and populate them.
async function downloadOffline() {
  var resources = [];
  var contentCache = await caches.open(CACHE_NAME);
  var currentContent = {};
  for (var request of await contentCache.keys()) {
    var key = request.url.substring(origin.length + 1);
    if (key == "") {
      key = "/";
    }
    currentContent[key] = true;
  }
  for (var resourceKey of Object.keys(RESOURCES)) {
    if (!currentContent[resourceKey]) {
      resources.push(resourceKey);
    }
  }
  return contentCache.addAll(resources);
}
// Attempt to download the resource online before falling back to
// the offline cache.
function onlineFirst(event) {
  return event.respondWith(
    fetch(event.request).then((response) => {
      return caches.open(CACHE_NAME).then((cache) => {
        cache.put(event.request, response.clone());
        return response;
      });
    }).catch((error) => {
      return caches.open(CACHE_NAME).then((cache) => {
        return cache.match(event.request).then((response) => {
          if (response != null) {
            return response;
          }
          throw error;
        });
      });
    })
  );
}
