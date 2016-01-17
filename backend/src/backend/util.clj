(ns backend.util
  (:require [backend.db.core :refer [clear-db!]]
            [backend.face :refer [clear-group group]]))

(defn clear
  []
  (clear-db!)
  (clear-group group))
