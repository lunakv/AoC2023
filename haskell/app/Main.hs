module Main (main) where
import Lib
import System.IO
import System.Environment (getArgs)

import qualified Day02
import qualified Day03

runners :: [(String, IO String -> IO ())]
runners =
  [ ("02", Day02.run)
  , ("03", Day03.run)
  ]

getRunner :: String -> IO String -> IO ()
getRunner day = head . map snd . filter ((== day) . fst) $ runners


headerDispatch :: String -> InputType -> IO ()
headerDispatch day input = do
  putStrLn $ "==== Day " ++ day ++ " ===="
  dispatch day input
  putStrLn ""

dispatch :: String -> InputType -> IO()
dispatch day input = getRunner day $ getInput day input

getType :: [String] -> InputType
getType x = case x of
  "-t1":_ -> Test1
  "-t2":_ -> Test2
  _:xs    -> getType xs
  _       -> Input

getDay :: [String] -> IO String
getDay x = case x of
  "-i":_ -> putStr "Select Day: " >> hFlush stdout >> (pad <$> getLine)
  "-a":_ -> return "all"
  _:xs   -> getDay xs
  _      -> return . fst . last $ runners

main :: IO ()
main = do
  args <- getArgs
  day <- getDay args
  let input = getType args
  if day == "all" then foldMap (headerDispatch . fst) runners input else dispatch day input