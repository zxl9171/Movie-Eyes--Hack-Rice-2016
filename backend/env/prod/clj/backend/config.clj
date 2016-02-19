(ns backend.config
  (:require [clojure.tools.logging :as log]))

(def defaults
  {:init
   (fn []
     (log/info "\n-=[backend started successfully]=-"))
   :middleware identity})
