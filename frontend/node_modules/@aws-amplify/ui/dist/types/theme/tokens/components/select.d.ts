import { DesignTokenProperties, OutputVariantKey } from '../types/designToken';
type SelectSizeTokens<Output> = DesignTokenProperties<'minWidth' | 'paddingInlineEnd', Output>;
type SelectIconWrapperTokens<Output> = DesignTokenProperties<'alignItems' | 'position' | 'top' | 'right' | 'transform' | 'pointerEvents', Output> & {
    small?: DesignTokenProperties<'right', Output>;
    large?: DesignTokenProperties<'right', Output>;
};
export type SelectTokens<Output extends OutputVariantKey> = DesignTokenProperties<'paddingInlineEnd' | 'whiteSpace' | 'minWidth', Output> & {
    wrapper?: DesignTokenProperties<'cursor' | 'display' | 'flex' | 'position', Output>;
    iconWrapper?: SelectIconWrapperTokens<Output>;
    option?: DesignTokenProperties<'backgroundColor' | 'color', Output> & {
        _disabled?: DesignTokenProperties<'color', Output>;
    };
    small?: SelectSizeTokens<Output>;
    large?: SelectSizeTokens<Output>;
};
export declare const select: Required<SelectTokens<'default'>>;
export {};
