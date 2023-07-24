Private  Function arm_capacity(v, e, l, r, icd, phi, circulatory_flow)
    arm_capacity = kx(Phi, r) * (Fx(x2x(v, e, Sx(e, v, l))) - fcx(x2x(v, e, S(e, v, l)), e, icd) * circulatory_flow)
End Function

Private  Function kx(phi, r)
    kx = 1 - 0.00347 * (phi - 30) - 0.978 * ((1 / r) - 0.05)
End Function

Private  Function Fx(x2x)
    Fx = 303 * x2x(v, e, s)
End Function

Private  Function fcx(e, icd, v, e)
    fcx = (0.210 * td(e, icd)) * (1 + 0.2 * x2x(v, e, l))
End Function

Private  Function td(v, e, icd)
    td = 1 + (0.5 / (1 + pow(e, ((icd - 60) / 10))))
End Function

Private  Function x2x(v, e, s)
    x2x = v + ((e-v) / 1 + 2 * s)
End Function

Private  Function Sx(e, v, l)
    Sx = (1.6 * (e - v)) / l
End Function

Function JUNCTION_CAP(od as Range, geometry as Range) As Variant
    Dim od As Variant
    Dim geometry As Variant
    Dim output As Variant
    
    arr_od = od.Value
    arr_geom = geometry.Value

    If arr_od.Rows.Count <> arr_od.Columns.Count Then:
        JUNCTION_CAP = "ErrorL OD Matrix must have same number of rows and columns"
        Exit Function

            
