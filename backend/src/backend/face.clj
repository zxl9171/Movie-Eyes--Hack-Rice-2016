(ns backend.face
  (:require [clojure.java.io :as io]
            [clj-http.client :as client]
            [clojure.data.json :as json])
  (:import (com.youtu Youtu)
           (org.json JSONObject)))

(def app-id "")
(def secret-id "")
(def secret-key "")

(defn download-img
  [avatar-url]
  (let [img-path (str "tmp/" (rand-int 10000) ".img")]
    (io/copy
      (:body (client/get avatar-url {:as :stream}))
      (java.io.File. img-path))
    img-path))


(defn new-youtu []
  (new Youtu app-id secret-id secret-key (Youtu/API_YOUTU_END_POINT)))

(defn res-path [name]
  (-> name io/resource .toURI .getPath))

(def face-youtu (new-youtu))

(def group "1")

(defn to-map 
  [json-obj]
  (-> json-obj str json/read-str))

(defn add-person [person-id person-img-path]
  (println (.NewPerson face-youtu person-img-path person-id [group])))

(defn add-local-img-to-person [person-id local-img-path]
  (.AddFace face-youtu person-id [local-img-path]))

(defn add-image-to-person [person-id person-img-path]
  (let [local-img (download-img person-img-path)]
    (add-local-img-to-person person-id local-img)))

(defn list-persons [groupid]
  (-> (.GetPersonIds face-youtu groupid)
      to-map
      (get "person_ids")))

(defn delete-person [person-id]
  (.DelPerson face-youtu person-id))

(defn clear-group [group-id]
  (doseq [person-id (list-persons group-id)]
    (delete-person person-id)))

(defn get-person-info [people-id]
  (-> (.GetInfo face-youtu people-id)
      to-map))

(defn face-identify [person-img-path]
  (println person-img-path)
  (let [json-obj (.FaceIdentify face-youtu person-img-path group)
        identify-result (json/read-str (str json-obj))
        error-message (identify-result "errormsg")]
    (do
      (println identify-result)
      (when (= error-message "OK")
        (-> identify-result
            (get "candidates")
            (first)
            (get "person_id"))))))
