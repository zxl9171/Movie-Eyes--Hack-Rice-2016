(ns backend.routes.home
  (:require [backend.layout :as layout]
            [compojure.core :refer [defroutes GET POST]]
            [ring.util.http-response :refer [ok]]
            [backend.db.core :refer :all]
            [clojure.java.io :as io]
            [backend.face :refer :all]))

(defn home-page []
  (layout/render
    "home.html" {:docs (-> "docs/docs.md" io/resource slurp)}))

(defn about-page []
  (layout/render "about.html"))

(defn add-image-page []
  (layout/render "addImage.html" {:actors (list-actor)}))

(defn add-image
  [name img-url]
  (add-image-to-person name img-url)
  (layout/render "addImage.html" {:actors (list-actor)
                                  :message "Add success"}))

(defroutes home-routes
  (GET  "/" [] (home-page))
  (GET  "/about" [] (about-page))
  (GET  "/add_image" [] (add-image-page))
  (POST "/add_image" req
        (let [{:keys [name image_url]} (:params req)]
          (add-image name image_url))))

