(ns backend.routes.services
  (:require [ring.util.http-response :refer :all]
            [compojure.api.sweet :refer :all]
            [clojure.string :as str]
            [clojure.java.io :as io]
            [clojure.data.codec.base64 :as b64]
            [clojure.data.json :as json]
            [clj-http.client :as client]
            [schema.core :as s]
            [backend.db.core :refer :all]
            [backend.face :refer :all]))

(s/defschema Thingie {:id Long
                      :hot Boolean
                      :tag (s/enum :kikka :kukka)
                      :chief [{:name String
                               :type #{{:id String}}}]})

(s/defschema UploadImg {:image-data s/Str})

(s/defschema Information {:name s/Str
                          :avatar s/Str
                          :films [s/Str]
                          :birth_date s/Str
                          :related_pics [s/Str]
                          :news [s/Str]
                          :bio s/Str})

(defn download-avatar
  [avatar-url temp-file-name]
  (io/copy
    (:body (client/get avatar-url {:as :stream}))
    (java.io.File. temp-file-name)))

#_(download-avatar "http://www.metasoarous.com/content/images/2014/12/profile1-1.jpeg" "profile.jpg")

(defn add-actor-info 
  "Handle incomint actor information"
  [{:keys [name avatar films birth_data related_pics] :as info}]
  (print info)
  (let [temp-pic-name (str "tmp/" name (rand-int 100000) ".jpg")]
    (download-avatar avatar temp-pic-name)
    (add-person name temp-pic-name)
    (create-actor! {:name name :avatar avatar :information (json/write-str info)})
    "Success!"))

(defn save-img-to-file
  [canvas-img-base64]
  (let [img-data (second (str/split canvas-img-base64 #","))
        img-file-path (str "tmp/" (rand-int 100000) ".img")]
    (with-open [in  (io/input-stream (.getBytes img-data))
                out (io/output-stream img-file-path)]
      (b64/decoding-transfer in out))
    img-file-path))

(defn dbg [x]
  (print x) x)

(defapi service-routes
  (ring.swagger.ui/swagger-ui
    "/swagger-ui")
  ;JSON docs available at the /swagger.json route
  (swagger-docs
    {:info {:title "Sample api"}})
  (context* "/api" []
            :tags ["Image Recongize"]
            (POST* "/recongize" []
                   ;; :return (s/maybe Information)
                   :body   [img UploadImg]
                   :summary "Upload imagine and return recognize result"
                   (let [local-img-file-name (save-img-to-file (:image-data img))
                         identify-result (face-identify local-img-file-name)]
                     (println identify-result)
                     (if identify-result 
                       (-> (get-actor {:name identify-result})
                           first
                           :information
                           json/read-str
                           ok)
                       (not-found {:error "Actor not found"}))))
            (OPTIONS* "/recongize" [] (ok "Hello"))
            (POST* "/info" []
                   :body [info Information]
                   :summary "Upload actor informations"
                   (ok (add-actor-info info)))))
