{-# LANGUAGE OverloadedStrings #-}

module Plots where

import Data.List (isInfixOf)
import qualified Data.ByteString.Lazy as BSL
import qualified Graphics.Vega.VegaLite as VL
import System.Process.ByteString.Lazy (readProcessWithExitCode)
import Data.Aeson (encode)
import qualified Data.Text as T

writeSpec :: FilePath -> VL.VegaLite -> IO ()
writeSpec x vlspec = BSL.writeFile x $ encode $ VL.fromVL vlspec

writeSvg :: FilePath -> VL.VegaLite -> IO ()
writeSvg x vlspec = do
  (ecode, stdout, stderr) <-
          readProcessWithExitCode "vl2svg" [] $ encode $ VL.fromVL vlspec
  --BSL.writeFile "out.vl" vlspec
  BSL.writeFile x stdout

writePng :: FilePath -> VL.VegaLite -> IO ()
writePng x vlspec = do
  (ecode, stdout, stderr) <-
          readProcessWithExitCode "vl2png" [] $ encode $ VL.fromVL vlspec
  --BSL.writeFile "out.vl" vlspec
  BSL.writeFile x stdout

channelPlot :: [T.Text] -> VL.VegaLite
channelPlot codeContributions =
  let
    channels = [\x a -> if "nix" `T.isInfixOf` T.toLower x then "other nix" else a,
                \x a -> if "ngi-nix" `T.isInfixOf` x then "ngi" else a,
                \x a -> if "NixOS/nixpkgs" `T.isInfixOf` x then "nixpkgs" else a]
    annotate x = foldl (\a func -> func x a) "other" channels
    vldata = VL.dataFromColumns []
        . VL.dataColumn "contribution" (VL.Strings codeContributions)
        . VL.dataColumn "channel" ( VL.Strings (annotate <$> codeContributions))
    marks = VL.mark VL.Bar
    encoding = VL.encoding 
        . VL.position VL.X [VL.PName "channel", VL.PmType VL.Nominal]
        . VL.position VL.Y [VL.PAggregate VL.Count, VL.PmType VL.Quantitative ]
  in VL.toVegaLite [vldata [], marks [], encoding [], VL.width 500, VL.height 500, customStyle []]

customStyle :: [VL.ConfigureSpec] -> VL.PropertySpec
customStyle =
  VL.configure
    . VL.configuration
      ( VL.Axis
          [ VL.Domain False,
            VL.LabelColor "#000000",
            VL.LabelPadding 4,
            VL.TickColor "#7F7F7F",
            VL.TickSize 5.67,
            VL.Grid True,
            VL.GridColor "#FFFFFF"
          ]
      )
