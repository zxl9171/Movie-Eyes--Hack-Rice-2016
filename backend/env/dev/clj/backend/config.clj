(ns backend.config
  (:require [selmer.parser :as parser]
            [clojure.tools.logging :as log]
            [backend.dev-middleware :refer [wrap-dev]]))

(def defaults
  {:init
   (fn []
     (parser/cache-off!)
     (log/info "\n-=[backend started successfully using the development profile]=-"))
   :middleware wrap-dev})
